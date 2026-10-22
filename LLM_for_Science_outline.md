# Large Language Models in Data Science

**2026–2027 · 21 hours · revised 19 October 2026**

## Message to students

The central story is **LLM → tools → feedback loop → complete data science workflow**. With data access and connected tools, agents can collect and join data, prepare it, explore it, build and evaluate models, produce interactive dashboards, choose actions under stated objectives, and automate processes. They can monitor outcomes and react to new data by repeating or revising the work.

That puts the traditional junior role under pressure. If your only offer is routine work done manually, you are in a bad position. Problem framing, model selection, and explanation can also be assisted; calling them human skills does not establish that they are protected. The question is what contribution you can demonstrate when a connected agent can attempt the whole workflow. How do you gain experience when entry-level practice work can be automated?

The lecture's blunt message is: **get your ass in gear — learn to build, use, and evaluate these systems.** We will study the full workflow through concrete tasks and a small working agent. Performance means useful, checked work completed with less time or cost, including review and repair.

We begin with the same illustrated introduction as last year. Tokens, embeddings, self-attention, transformers, and next-token prediction give you the mental model needed for the practical work. The architecture develops through the slides: open the embedding predictor's feed-forward network, add a recurrent hidden state to connect positions, then introduce attention while retaining feed-forward layers. We end with the Python exercise extended into an agent: generate code, execute it separately, inspect feedback, and revise within a fixed budget.

The Week 1 opening follows one assignment throughout: customers are leaving; find what changed and what to do. First trace the data–action loop, then introduce the language model and its outputs before explaining tools or agents. Show how generated Python becomes executed work through feedback and checks. Extend that pattern across the churn analysis, dashboard, decision, intervention, and measured outcomes. This gives each slide a dependency on the previous one.

Then move from the workflow to organisations and society. If useful analysis becomes cheaper, organisations can expand their work, compress staffing, or reorganise roles around automated workflows. These are scenarios to discuss. Employer expectations of growth in data/AI roles and observed pressure on young workers measure different things; neither establishes a fixed future for data science. At society level, ask who can access the technology, who receives the gains or bears the losses, and who controls decisions. Close the opening with the students' response and the course route, then begin the technical explanation with text becoming numbers. See the [work and society sources](docs/references.md#work-data-science-and-society).

The architecture supplies practical guidance. In **red toy robot**, `toy` changes the kind of object; attention lets its information affect the vector at `robot`. Later, prompts must supply the relevant facts, units, definitions, and constraints, and agent calls must receive current observations. A context window is finite, so select useful information rather than assuming more text is better. Sampling explains variation between generated continuations. Next-token probability is not a truth score: check sources, recompute numbers, and test code. Lower temperature can reduce variation without establishing correctness. Hallucination also depends on training and uncertainty; it is not explained by attention or sampling alone. See the [architecture-to-practice sources](docs/references.md#week-1-from-architecture-to-practice).

Keep one architecture sequence: **RNN context → attention → Transformer blocks → encoder and decoder roles → training → generation**. The RNN diagram introduces the context carried through `red toy robot`; its historical translation figures remain optional material. Finish the attention example by adding its contribution to the original vector. One overview then shows successive Transformer blocks updating the token representations; detailed residual paths and next-block query/key/value calculations remain optional. Define encoders and decoders as stacks of blocks on consecutive slides: the encoder uses the complete supplied input, while decoder self-attention uses only the text so far. Immediately connect them in the translation diagram: French output reaches decoder self-attention; English encoder vectors reach cross-attention. Return to GPT-style models with one training slide: known text supplies the next-token target, loss measures the prediction error, and feedback updates the model weights. Then use the learned weights for generation, where prompt and continuation form one sequence, and follow token choice through generation settings. Show where context enters once, without repeating embedding lookup or query/key/value arithmetic.

The technical sequence still starts with the basics: understand the model (Weeks 1–2), direct and evaluate it on tasks (Weeks 3–4), supply evidence and build the loop (Week 5), then demonstrate a measured result (Week 6).

Audience: final-year data science students. Prerequisites: Python/Jupyter, statistics, and basic machine learning. The same methods apply to scientific datasets, papers, and reports.

## Sequence

Keep the original six teaching blocks and the approximately 7-hour lecture / 7-hour lab / 7-hour hackathon allocation. The 90-minute labels in individual decks are planning guides; pace the first five blocks to fit the 14 available hours.

| Week | Lecture | Practical work |
|---|---|---|
| 1 — LLMs: a primer | Text representations, tokenization, embeddings, neural networks, autoregressive prediction, self-attention, transformer blocks, training versus inference. Keep the original figures and worked explanations. | Compare tokenizers, inspect embeddings and similarities, explain the prediction path. |
| 2 — Hugging Face | Choose a checkpoint; trace a pipeline into tokenization, model scores and labels; apply generation settings; introduce chat templates; measure batching, quality and runtime. | Retain the original DistilBERT/BERT sentiment comparison and GPT-2 example. Record exact revisions and compare balanced IMDB examples. Chat, precision and hosted inference remain optional. [First-revision notes](docs/week_2_review.md). |
| 3 — From a task to a verified analysis | Follow one churn question: define the task and context, inspect a hosted API call, distinguish JSON parsing, schema validation and factual correctness, then generate, execute and check Python. Revise from actual results. | Predict the six-row result; validate structured JSON; generate and inspect loading and analysis functions; improve the plot; check the same code on all 600 rows. Compare full-CSV and generated-code routes on correctness, tokens and cost. Finish with confidence intervals, a test of association between contract type and churn, and a supported conclusion. Students write their own prompts and implementation. Label saved examples when live calls or code execution are skipped. |
| 4 — Classification and evaluation | Preserve the four-method AMU comparison: regex rules, embeddings with logistic regression, a pretrained classifier and a prompted LLM. Define labels, training/development/test splits, accuracy, precision/recall, prediction time and API token usage. | Compare the four methods on development data. Use an LLM to suggest a regex revision and generate ten synthetic debugging requests. Review the labels, improve one method, then evaluate all four on the same separate test set. Count invalid outputs and API failures. |
| 5 — Evidence and agent loops | Follow the student-service questions from full-document context to RAG, then an answer–review loop with at most four attempts. Collect official AMU webpages and compare our RAG with web search. | Build a searchable collection from selected AMU pages, retaining URLs and download dates. Compare RAG, RAG with review, and a model with web search on the same questions. Keep the model fixed first, then compare another model; verify facts and citations and measure total time and cost. |
| 6 — Hackathon | Existing briefing, team project, demonstrations, and discussion. | Deliver a reproducible project and compare quality, total time, and API usage/cost with a baseline. |

## What students should be able to do

1. Explain how text passes through tokenization, embeddings, attention, and next-token prediction.
2. Use pretrained models and APIs, recording the model and generation settings.
3. Specify an analysis, parse its outputs, and check calculations and conclusions against the data.
4. Compare classification methods and choose between direct document context and retrieval.
5. Implement a small model–tool–observation loop with allowed tools, execution limits, and a verified stopping condition.
6. Explain where AI improved a workflow and where review or repair consumed the apparent gain.

## Retrieval and loops

RAG is still useful: it supplies selected evidence to generation. A small corpus may fit directly into the prompt, so retrieval is a choice to test rather than a requirement. Compare answer quality, source support, latency, and cost. A long context window does not guarantee use of every relevant fact. See [Google's long-context guidance](https://ai.google.dev/gemini-api/docs/long-context).

Week 4 establishes classification and evaluation on student-service requests. Week 5 changes the task to answering those questions from documents; classification is not a prerequisite. Preserve the evaluation discipline: development questions for improvements, separate final questions, independently checked facts and sources, and complete time/cost measurements. The main workflow retrieves evidence, drafts an answer, reviews it in a second call and revises from feedback. After the small teaching example, students build a collection from official AMU webpages and compare it with web search. A second model adds a comparison of complete systems; keeping the model fixed first helps distinguish the effect of information access.

The Week 5 loop follows **question → retrieve → answer → review → revise**. Both model calls receive the question and sources. Stop when the reviewer accepts the answer, identifies missing information, or the workflow reaches four attempts. Students independently verify the final answers and citations; the reviewer is part of the system being evaluated.

Students collect selected public AMU pages with a Python download/extraction tool, then keep the saved corpus fixed for repeated RAG runs. The web-search comparison may use newer or additional sources; preserve URLs and run dates so those differences can be inspected.

## Assessment and materials

Lectures are screens off: listen, ask questions, discuss, and sketch ideas on paper. Labs are individual work with tools, including AI assistance; discussion is allowed, and students must be able to explain and check their own work.

The final evaluation is one hackathon day: teams of 1–5 build a working product with an agent loop that calls tools, receives observations, and revises the work. Demonstrate the product and a real loop trace, explain the course concepts applied, and show a stopping condition and completion check. Presentations last 5–7 minutes. The four criteria remain worth 5 points each — Use Case & Applications, Code Cleanliness, Lecture Integration, and Presentation. Compare with a baseline and report quality, total time (including review and repair), API usage/cost, and a failure/revision example. No required speedup factor. A local working product is sufficient; public deployment is optional.

Reusable slides, labs, and datasets remain in Git. Private student work, grades, solutions, and instructor notes stay under ignored `local/student/` and `local/instructor/` directories. Last year's lecture is preserved on `archive/2025-2026`.

## Further study

Use selected [Stanford CS336 recordings](https://cs336.stanford.edu/) for the foundations and [Hugging Face's agent cycle](https://huggingface.co/learn/agents-course/en/unit1/introduction) for the last block. The [reference list](docs/references.md) includes recent university lectures, the Google/Kaggle agent courses, and Andrew Ng's video course. [Revision notes](docs/2026_revision.md) identify the limited changes and their sources.
