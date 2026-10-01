# Large Language Models in Data Science

**2026–2027 · 21 hours · revised 1 October 2026**

## Message to students

LLMs can do much of the routine work assigned to a junior data scientist: prepare data, write Python, fit models, draw figures, and draft explanations. This course teaches you to turn that capability into better performance. You will learn how the models work, use them on concrete tasks, and check the results. Performance means useful, correct work completed with less time or cost; fluent answers alone do not establish it.

We begin with the same illustrated introduction as last year. Tokens, embeddings, self-attention, transformers, and next-token prediction give you the mental model needed for the practical work. We end with the Python exercise extended into an agent: generate code, execute it separately, inspect feedback, and revise within a fixed budget.

Audience: final-year data science students. Prerequisites: Python/Jupyter, statistics, and basic machine learning. The same methods apply to scientific datasets, papers, and reports.

## Sequence

Keep the original six teaching blocks and the approximately 7-hour lecture / 7-hour lab / 7-hour hackathon allocation. The 90-minute labels in individual decks are planning guides; pace the first five blocks to fit the 14 available hours.

| Week | Lecture | Practical work |
|---|---|---|
| 1 — LLMs: a primer | Text representations, tokenization, embeddings, neural networks, autoregressive prediction, self-attention, transformer blocks, training versus inference. Keep the original figures and worked explanations. | Compare tokenizers, inspect embeddings and similarities, explain the prediction path. |
| 2 — Hugging Face | Checkpoints, tokenizers, model heads, forward passes, generation, decoding, batching, devices, and memory. | Load pretrained models and compare their outputs and inference settings. Older small models illustrate mechanics. |
| 3 — Effective LLM use | Clear tasks, system/user instructions, context, output formats, prompt revision, coding, research, and analysis. | Retain the role and JSON exercises. Generate `analyze(df)` for the churn dataset, execute in a separate Docker environment, inspect statistics and plots. |
| 4 — Classification and routing | Rules, embeddings with logistic regression, zero-shot classification, and prompted LLMs; accuracy and latency. | Retain the AMU chatbot task. Compare methods on held-out cases and count invalid outputs/API failures. |
| 5 — Retrieval, then agent loops | Retain the RAG diagrams and explanations: chunking, BM25, embeddings, hybrid retrieval, metadata filters, and source support. First compare retrieval with full-document context. Finish with tools, observations, revisions, and stopping rules. | Keep the retrieval notebook; deeper retrieval experiments are optional. Extend generated Python into an agent loop with execution feedback and independent checks. Compare with provider-managed code execution. |
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

The final agent follows **task → propose code/tool call → validate → execute → observe → revise**. Stop after a verified result or a step/time limit. A dictionary of Python globals does not isolate generated code; use a separate execution environment. The checks run outside that environment. Revising code from feedback changes the workflow, not the model's weights.

Managed tools can provide execution and frameworks can dispatch calls, but students should first understand the small loop they can inspect. Retrieval can later become one of its tools.

## Assessment and materials

Keep the original hackathon: teams of 1–5, presentations of 5–7 minutes, four criteria worth 5 points each — Use Case & Applications, Code Cleanliness, Lecture Integration, and Presentation. Add measured quality, total time (including review and repair), API usage/cost, and a failure/revision example to the evidence presented. No required speedup factor.

Reusable slides, labs, and datasets remain in Git. Private student work, grades, solutions, and instructor notes stay under ignored `local/student/` and `local/instructor/` directories. Last year's lecture is preserved on `archive/2025-2026`.

## Further study

Use selected [Stanford CS336 recordings](https://cs336.stanford.edu/) for the foundations and [Hugging Face's agent cycle](https://huggingface.co/learn/agents-course/en/unit1/introduction) for the last block. The [reference list](docs/references.md) includes recent university lectures, the Google/Kaggle agent courses, and Andrew Ng's video course. [Revision notes](docs/2026_revision.md) identify the limited changes and their sources.
