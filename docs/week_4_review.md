# Week 4 — slide and notebook revision

21 October 2026. Slides jointly reviewed with the instructor; notebook revised to
follow the accepted sequence and the recorded [teaching skill](../skills/course-lecture-review/SKILL.md).
The README now links the revised Week 4 materials.

## Main finding

The archived Week 4 was a nine-slide briefing for the lab. It already included
the same four methods, including “Zero-shot NLI pipeline” in its overview and
“Zero-shot classification (MNLI)” in its methods slide. Module 4 of the archived
notebook already used `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`. NLI is not a new
addition this year.

The first revision expanded this brief comparison too much. In particular, the
extra terminology and three-relation NLI explanation made the practical operation
harder to follow. The joint review has removed that detour and “token by token”.
The main slides now show the inputs and outputs of the original method; its NLI
internals remain in speaker notes. Preserve last year's practical emphasis when
continuing the review, rather than adding theory simply because it is available.

The revision keeps the AMU service-routing example, portal image, five service
labels and four methods. It expands explanations rather than adding classifier
families. The new route is **define the task → explain each method → measure the
same task fairly → improve using development errors → justify a choice**.

## Slide-by-slide route

| Slide | Purpose and change |
|---|---|
| 1 | Keep the course identity; make comparison the session's purpose. |
| 2 | Connect Week 3's checked workflow with choosing a method for a repeated task. |
| 3 | Keep the portal image and show request → classifier → service label. Distinguish routing from executing the service action. |
| 4 | Define intent and label, then show all five codes with intent descriptions and French examples. Use “intent” consistently instead of introducing “requested service” for the same categories. |
| 5 | Show three straight arrows splitting labelled requests into training, development and test sets. Training and development determine a selected method; a distinct arrow labelled “Final candidate” carries it to evaluation, which receives the held-out test data separately. |
| 6 | Use practical input/output descriptions: the pretrained classifier receives the request and five intent descriptions and returns scores; the prompted LLM is asked to return a label. No zero-shot detour or token-generation detail. |
| 7 | Show an actual regex rule using `re.search`, explain `|` as “or”, and show a missing match: `email` does not match `e-mail`. |
| 8 | Reuse sentence embeddings: request → pretrained model → one 384-dimensional vector. Keep the original multilingual MiniLM. |
| 9 | Explain what logistic regression learns and how it predicts. Define the standard score formula, weights, bias and selected class. Keep the embedding model fixed. |
| 10 | Pair every existing label with its description, reusing the wording from slide 4. Explain that multilingual mDeBERTa was trained to judge whether a text supports a statement. Use the student-email request to illustrate how it scores each intent; select the highest-scoring label. Remove the redundant dictionary-lookup diagram. Keep NLI internals in speaker notes. |
| 11 | Reuse Week 3's system/user distinction; show the five-label instruction and desired JSON reply. Explain that the model generates text which we parse and check. |
| 12 | Separate parsing/allowed-label validation from correctness, including no response or no matching rule. |
| 13 | Define accuracy using every test request. Show explicitly illustrative counts, including invalid outputs and API failures. |
| 14 | Use those same 50 illustrative cases in a confusion matrix, including a separate no-label column. |
| 15 | Derive library recall and precision directly from that matrix. |
| 16 | Measure only the time to obtain a label with the model already loaded, excluding training, and the input/output tokens reported by the API. Remove the method-by-method breakdown. |
| 17 | Use the missed email request to ask an LLM for a regex revision. Show `e-?mail`, explain the optional hyphen, and compare corrected predictions and new errors on the development set. The proposed revision is an illustration, not a claimed API response. |
| 18 | Give an LLM prompt to generate ten synthetic French debugging requests, two per existing label, with varied wording, abbreviations and typos. Students check the labels, run the classifier and use mistakes to revise it on the development set. |
| 19 | Preview Week 5 with a lost-student-card request: this week predicts a label; next week uses university documents to answer the question. Define added context as the supplied passage and an agent loop as searching again and inspecting the result when information is missing. |
| 20 | Set out the individual lab workflow and the decision students must justify. |
| 21 | Link primary documentation for the methods and evaluation. |

The original deck labelled the lecture as a 15-minute briefing. The first revision
removed that time label while expanding the deck. The instructor's preference is
to retain the original's clarity and practical focus; slide count and pacing should
serve that purpose rather than justify expansion. The joint slide review is complete.

## Decisions from the slide review

- Keep five service labels for the main comparison. Greetings and unrelated
  requests are valuable follow-up cases, but a seven-label experiment must give
  every method a way to predict all seven labels. Adding them only to the LLM is
  not a fair comparison. Multi-intent requests need a stated policy as well.
- NLI is not required for the course's later workflow or evaluation concepts.
  Retain it as one brief worked baseline from the original four-method comparison:
  a pretrained classifier can test new intent descriptions without fitting on
  AMU examples. The extra candidate-statement slide and the three-relation theory
  diagram have been removed. Do not expand it into a separate theory section or
  introduce zero-shot terminology merely to defend the previous method name.
- Keep model-specific loading and API code in the lab, since Weeks 2–3 already
  teach those mechanics. The lecture now concentrates on what each method does
  and how to assess the result.
- The numerical examples teach metrics; they are not benchmark measurements.
  The empty method-comparison slide was removed during the joint review.
- Document context and agents follow the baseline comparison. Do not add a loop
  just to make the exercise sound current. Ask which observed failure requires
  further information or actions and measure the complete resulting workflow.

## Notebook revision

The notebook retains the original 50 training requests and all four classifiers.
The sequence follows the reviewed slides, with demonstrations separated from
student exercises.

- **One label set:** the same five labels and descriptions are used throughout.
  The LLM no longer has additional `chat` and `unknown` labels.
- **Separate data:** ten initial development requests, plus ten LLM-generated
  debugging requests after student review. A separate file contains 20 new,
  hand-written synthetic test requests, four per label. The test file is loaded
  only after development; exact duplicates are checked across splits. Students
  also review generated requests for near-copies and ambiguous labels.
- **Actual regex:** `re.search` replaces the old substring loop. The lecture's
  `email`/`e-mail` example motivates an LLM suggestion, followed by a before/after
  development comparison. The original rules are retained.
- **Model explanation:** inspect the 384-dimensional sentence vector, fit logistic
  regression, then inspect the pretrained classifier's description scores.
  The pipeline's required task identifier is explained briefly beside the code.
- **Common API:** replace the mismatched OpenAI/Gemini code with the Week 3 Gemini
  client and `gemini-3.5-flash-lite`. API cells run directly without extra flags.
  JSON labels are validated; a failed call or invalid reply is recorded.
- **Measured comparison:** reference labels, predictions, failure types, prediction
  time and reported API tokens are saved per request. Model loading and fitting
  happen before timing. Local execution selects CPU, CUDA/ROCm or Apple MPS.
  Accuracy includes failed predictions; missing token usage is not counted as zero.
- **Exercises:** interpret precision and recall from the confusion matrix; inspect
  the proposed regex and add two checks; review synthetic labels; improve one
  method and compare corrected predictions with new errors. No predetermined
  winner, partner assignment, submission step or completed final exercise.
- **Private outputs:** generated data, suggestions, predictions and settings go
  under `local/student/2026-2027/week_4/`. The shared notebook has no saved outputs.

The development comparison sends ten classification API calls; the final test
sends twenty. The initial demonstration, regex suggestion and synthetic-data
request add three calls. Student experiments can add more. Final classification
usage excludes those earlier development calls.

## Sources checked

Primary documentation checked on 21 October 2026:

- [scikit-learn: data leakage and common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html).
- [scikit-learn: classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics).
- [Multilingual MiniLM model card](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2): sentence embeddings with 384 dimensions.
- [Hugging Face zero-shot pipeline](https://huggingface.co/docs/transformers/en/main_classes/pipelines#transformers.ZeroShotClassificationPipeline)
  and [the retained multilingual NLI model](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli).

## Validation

The revised deck now has 21 pages after merging the two NLI slides and removing the empty comparison-table slide. The PDF was
rebuilt with pdfLaTeX; changed pages were rendered and visually inspected, after
the initial full-deck inspection. Content has no overfull boxes; the shared theme's existing
title-bar width warnings remain. The worked counts are consistent: 43 correct,
five wrong labels and two requests without a label, from 50 total requests;
library recall is 8/10 and precision is 8/9. No benchmark measurements are invented. A compiled deck is not evidence of classifier
accuracy or speed.

The notebook was run from start to finish with the cached MiniLM and mDeBERTa
models on CPU and simulated Gemini replies, with network access disabled. This
checked 40 development prediction records and 80 final prediction records,
CSV parsing, duplicate checks, metrics, plots and local output files. The plots
were inspected. No simulated model results were saved in the shared notebook.
Live Gemini access and Apple MPS execution were not tested.

Six focused offline tests cover split separation, regex revision, valid/invalid
JSON, token accounting and failed predictions in the accuracy denominator.
Notebook structure and Python syntax checks pass. The repository skill passes
its validator.
