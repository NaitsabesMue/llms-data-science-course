"""Answer--review loop for Week 5; no API calls or credentials on import.

Retrieve passages with the full question using the lab's retrieval function.
For the French question and English documents, use multilingual embeddings.
Then bind the Week 3 client/model to the two API functions:

    from functools import partial
    writer = partial(write_answer, client, model_name)
    reviewer = partial(review_answer, client, model_name)
    result = run_loop(writer, reviewer, question, passages)

Both calls can use the same model. Reviewer acceptance is not proof of correctness.
"""
import json
from pathlib import Path

example = json.loads(Path(__file__).with_name('documents.json').read_text())
documents = example['documents']
question = example['question']

ANSWER_INSTRUCTIONS = '''Answer the student's question in French using only the
supplied passages. Cite passage IDs beside the claims they support. If revising,
use the previous answer and reviewer feedback, but check feedback against the
passages. State explicitly when the passages lack information. Return the answer
as plain text.'''

REVIEW_INSTRUCTIONS = '''Review the answer against the original question and
supplied passages. Check that it addresses the question, that factual claims are
supported, and that citations identify the supporting passages.
Return JSON with exactly two fields: status and feedback.
status must be:
- accepted: the answer addresses the question and is supported by the passages;
- revise: the passages suffice, but the answer needs specific corrections;
- missing_information: the passages do not contain enough information to answer.
In feedback, explain the decision and give concrete corrections or identify the
missing information. Do not demand facts absent from the passages or assume that
missing information is unavailable elsewhere.'''


def write_answer(client, model_name, question, passages, previous_answer, feedback):
    response = client.models.generate_content(
        model=model_name,
        contents=json.dumps({'question': question, 'passages': passages,
                             'previous_answer': previous_answer, 'feedback': feedback}),
        config={'system_instruction': ANSWER_INSTRUCTIONS},
    )
    if not isinstance(response.text, str) or not response.text.strip():
        raise ValueError('The answering model returned no answer text.')
    return response.text


def check_review(review):
    if not isinstance(review, dict) or set(review) != {'status', 'feedback'}:
        raise ValueError('A review must contain status and feedback.')
    if review['status'] not in ('accepted', 'revise', 'missing_information'):
        raise ValueError('Unknown review status.')
    if not isinstance(review['feedback'], str) or not review['feedback'].strip():
        raise ValueError('A review must explain its decision in feedback.')


def review_answer(client, model_name, question, passages, answer):
    response = client.models.generate_content(
        model=model_name,
        contents=json.dumps({'question': question, 'passages': passages, 'answer': answer}),
        config={'system_instruction': REVIEW_INSTRUCTIONS,
                'response_mime_type': 'application/json'},
    )
    review = json.loads(response.text)
    check_review(review)
    return review


def run_loop(writer, reviewer, question, passages, max_attempts=4):
    """Keep passages fixed; revise with feedback for at most four attempts.

    writer and reviewer each make one call per attempt. Exceptions propagate;
    there are no hidden retries. A returned answer is always accompanied by its
    review and workflow status, including missing_information or attempt_limit.
    """
    if not isinstance(max_attempts, int) or not 1 <= max_attempts <= 4:
        raise ValueError('Choose between one and four attempts.')
    answer, feedback = '', ''
    trace = []
    for attempt in range(max_attempts):
        answer = writer(question, passages, answer, feedback)
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError('The answering model returned no answer text.')
        review = reviewer(question, passages, answer)
        check_review(review)
        trace.append({'attempt': attempt + 1, 'answer': answer, 'review': review})
        if review['status'] != 'revise':
            return {'status': review['status'], 'answer': answer,
                    'review': review, 'trace': trace}
        feedback = review['feedback']
    return {'status': 'attempt_limit', 'answer': answer,
            'review': review, 'trace': trace}
