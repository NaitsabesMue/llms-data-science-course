# Large Language Models in Data Science

**2026–2027 · 21 hours · English · Aix-Marseille Université**

LLMs can carry out many routine tasks assigned to a junior data scientist: write code, prepare data, produce plots, and draft an analysis. This course teaches you to use that work to improve your performance, and to check whether it actually helps. We start with tokens, embeddings, and self-attention, then use pretrained models and APIs. We finish by turning generated Python into a bounded agent loop: execute, inspect, and revise.

For final-year data science students with a strong mathematics background and working knowledge of Python, statistics, and machine learning.

## Course objectives

- Understand tokens, embeddings, transformer architecture, training, and inference.
- Use pretrained models through Hugging Face and hosted APIs.
- Write clear prompts, parse outputs, and check generated analyses.
- Compare rules, classical ML, model prompting, and retrieval on quality and latency.
- Build a small agent that uses execution feedback; measure quality, total time, and cost against a baseline.

## Structure and materials

Approximately 7 hours of lectures, 7 hours of labs, and a 7-hour hackathon. The six teaching blocks retain last year's order; adjust lecture/lab pacing to fit the timetable.

Week 1 is ready for the current course. Links to later weeks will be added as their materials are revised.

| Week | Topic | Slides | Lab |
|---|---|---|---|
| 1 | LLMs: a primer — tokens, embeddings, self-attention, transformers | [PDF](slides/week_1_intro.pdf) · [source](slides/week_1_intro.tex) | [Tokenization and embeddings](labs/week_1_tokenization.ipynb) |

The original illustrated introduction remains the foundation. RAG remains in the course, with a comparison against supplying the full document set. Detailed retrieval experiments are optional if more time is needed for the final agent loop.

See the [lecture outline](LLM_for_Science_outline.md), [recent lecture videos and readings](docs/references.md), and [revision notes](docs/2026_revision.md).

The Week 1 notebook retains the original whitespace, bag-of-words, news-tokenization, and MiniLM exercises. It adds the Qwen3.5 tokenizer, chat-format token counts, and a comparison of lookup and contextual vectors. An optional NumPy exercise follows the self-attention calculation. Core exercises need public downloads on their first run; hosted generation and the larger embedding comparison are disabled by default. Save student reports and tables under `local/student/2026-2027/week_1/`.

## Rules of the game

- **Lecture: screens off.** Listen, ask questions, discuss, and sketch ideas on paper.
- **Lab: collaborate and use tools.** Work together with laptops, AI assistants, and coding tools. Test the results and be able to explain your work.
- **Final evaluation: one hackathon day.** Build a working product around an agent loop: the model calls tools, receives observations, and revises the work. Demonstrate what you learned by showing the product and the loop running.

## Lab setup

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab labs
```

For hosted calls, install `requirements-live.txt` and set the relevant API key and model identifier in a local `.env` file; `.env.example` lists the variable names. Choose a model available to your account. Calls use account quota and may incur charges. Earlier Hugging Face models are retained to teach the mechanics.

The Week 3 EDA cell executes generated code in Docker. Start Docker and prepare its image before class:

```sh
docker build -t llm-course-eda -f labs/Dockerfile.eda .
docker pull python:3.13-slim
```

The Week 5 extension uses the smaller standard-library image. Both containers have execution limits and no runtime network access. Its offline example illustrates feedback with simulated observations; enable the live section to obtain a real model/tool trace. Managed execution alternatives are linked in [the references](docs/references.md).

## Final evaluation: hackathon

Teams of 1–5 students spend one day building a working product that uses an agent loop to complete a concrete task. A small application, dashboard, or service is enough if a user can run it and obtain a useful result. A local demo is sufficient; public deployment is optional.

Show the product working, a trace of tool calls and observations, a failure followed by a revision, and the check that decides when the task is complete. Explain which course concepts you used and why. The grading scheme remains four criteria worth 5 points each:

| Criterion | Points | Evidence |
|---|---:|---|
| Use Case & Applications | 5 | Relevant problem, useful result, comparison with a baseline |
| Code Cleanliness | 5 | Readability, organization, modularity, reproducibility |
| Lecture Integration | 5 | A working agent loop with tool use, feedback, a stopping condition, and checked results; explain other course methods used |
| Presentation | 5 | Clear demo, visuals, and explanation of decisions and limitations |

Compare with a simple baseline on the same tasks. Report quality, total time including review and repair, and API usage/cost. Keep the loop as simple as the task allows. Presentations remain 5–7 minutes; the score out of 20 is the course grade.

## Shared and private materials

Slides, reusable labs, and public/synthetic datasets stay in Git. Private submissions and student work go in `local/student/2026-2027/`; grades, solutions, and instructor notes go in `local/instructor/2026-2027/`. Run traces go in `local/runs/`. The whole `local/` directory is ignored; create these directories on a fresh clone. Submit private projects through the university teaching platform.

`main` is the current course. The local branch `archive/2025-2026` preserves the previous slides and labs, including the notebook edits present before this revision. No branch has been pushed as part of this revision.

Run `make slides` to rebuild the PDFs and `make check` for notebook checks and the agent tests. Hosted calls and Docker execution require their respective services and are separate from the offline checks.

Instructor: Sebastian Mueller · Aix-Marseille Université
