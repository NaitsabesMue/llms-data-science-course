"""Offline checks for the Week 5 answer--review example."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'slides/examples/week5_retrieval'
spec = importlib.util.spec_from_file_location('week5_example', EXAMPLE / 'workflow.py')
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


class Week5ExampleTests(unittest.TestCase):
    def setUp(self):
        # Supplied test fixtures, not claimed retrieval/model outputs.
        self.passages = [d for d in workflow.documents if d['id'] in {'D2', 'D3'}]

    def test_full_prompt_contains_actual_documents_and_same_question(self):
        prompt = (EXAMPLE / 'full_prompt.txt').read_text()
        self.assertIn(workflow.question, prompt)
        for doc in workflow.documents:
            self.assertIn(f"[{doc['id']}] {doc['text']}", prompt)

    def test_previous_answer_and_feedback_reach_writer(self):
        writes, reviews = [], []

        def writer(question, passages, previous_answer, feedback):
            writes.append((question, passages, previous_answer, feedback))
            return f'Illustrative answer {len(writes)}'

        def reviewer(question, passages, answer):
            reviews.append((question, passages, answer))
            if len(reviews) == 1:
                return {'status': 'revise', 'feedback': 'Include the photo ID instruction from D3.'}
            return {'status': 'accepted', 'feedback': 'Both instructions are supported.'}

        result = workflow.run_loop(writer, reviewer, workflow.question, self.passages)
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(len(result['trace']), 2)
        self.assertEqual(writes[0][2:], ('', ''))
        self.assertEqual(writes[1][2:], ('Illustrative answer 1', 'Include the photo ID instruction from D3.'))
        self.assertEqual(reviews[1], (workflow.question, self.passages, 'Illustrative answer 2'))
        self.assertEqual(writes[1][:2], (workflow.question, self.passages))

    def test_four_attempts_never_imply_acceptance(self):
        calls = []

        def writer(*args):
            calls.append('write')
            return 'Unaccepted draft.'

        def reviewer(*args):
            calls.append('review')
            return {'status': 'revise', 'feedback': 'Correct the unsupported claim.'}

        result = workflow.run_loop(writer, reviewer, workflow.question, self.passages)
        self.assertEqual(result['status'], 'attempt_limit')
        self.assertEqual(calls, ['write', 'review'] * 4)
        self.assertEqual(len(result['trace']), 4)

    def test_missing_information_stops_without_accepting(self):
        result = workflow.run_loop(
            lambda *args: 'No replacement price is supplied.',
            lambda *args: {'status': 'missing_information', 'feedback': 'No passage gives the price.'},
            'What does a replacement cost?', self.passages,
        )
        self.assertEqual(result['status'], 'missing_information')
        self.assertEqual(len(result['trace']), 1)

    def test_invalid_reviews_are_not_accepted(self):
        for review in [None, {'status': 'accepted'}, {'status': 'unknown', 'feedback': 'Why'},
                       {'status': 'accepted', 'feedback': ''}]:
            with self.subTest(review=review), self.assertRaises(ValueError):
                workflow.run_loop(lambda *args: 'Draft', lambda *args: review,
                                  workflow.question, self.passages)

    def test_writer_and_reviewer_receive_the_evidence(self):
        sent = []
        replies = iter(['Illustrative answer.', json.dumps({'status': 'accepted', 'feedback': 'Supported.'})])

        def generate_content(**kwargs):
            sent.append(kwargs)
            return SimpleNamespace(text=next(replies))

        client = SimpleNamespace(models=SimpleNamespace(generate_content=generate_content))
        answer = workflow.write_answer(client, 'test-model', workflow.question,
                                       self.passages, 'Old answer', 'Fix citations')
        review = workflow.review_answer(client, 'test-model', workflow.question, self.passages, answer)
        for call in sent:
            payload = json.loads(call['contents'])
            self.assertEqual(payload['question'], workflow.question)
            self.assertEqual(payload['passages'], self.passages)
        self.assertEqual(json.loads(sent[0]['contents'])['previous_answer'], 'Old answer')
        self.assertEqual(json.loads(sent[0]['contents'])['feedback'], 'Fix citations')
        self.assertEqual(json.loads(sent[1]['contents'])['answer'], answer)
        self.assertEqual(review['status'], 'accepted')

    def test_rejects_invalid_attempt_limits(self):
        for limit in (0, 5, 1.5):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                workflow.run_loop(None, None, workflow.question, self.passages, max_attempts=limit)


if __name__ == '__main__':
    unittest.main()
