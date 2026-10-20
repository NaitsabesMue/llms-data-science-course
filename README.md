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

Weeks 1–3 have been revised for the current course. Weeks 4–6 remain in the outline; their material links will be added after review.

| Week | Topic | Slides | Lab |
|---|---|---|---|
| 1 | LLMs: a primer — tokens, embeddings, self-attention, transformers | [PDF](slides/week_1_intro.pdf) · [source](slides/week_1_intro.tex) | [Tokenization and embeddings](labs/week_1_tokenization.ipynb) |
| 2 | Hugging Face — pretrained models, pipelines, generation and batching | [PDF](slides/week_2_huggingface.pdf) · [source](slides/week_2_huggingface.tex) | [Using pretrained models](labs/week_2_huggingface_basics.ipynb) |
| 3 | From a task to a verified analysis — API calls, generated Python and feedback | [PDF](slides/week_3_effective_llm_use.pdf) · [source](slides/week_3_effective_llm_use.tex) | [Generate, execute and check an analysis](labs/week_3_effective_llm_use.ipynb) |

The original illustrated introduction remains the foundation. RAG remains in the course, with a comparison against supplying the full document set. Detailed retrieval experiments are optional if more time is needed for the final agent loop.

See the [lecture outline](LLM_for_Science_outline.md), [recent lecture videos and readings](docs/references.md), and [revision notes](docs/2026_revision.md).

The Week 1 notebook retains the original whitespace, bag-of-words, news-tokenization, and MiniLM exercises. It adds the Qwen3.5 tokenizer and a comparison of lookup and contextual vectors. An optional NumPy exercise follows the self-attention calculation. Core exercises need public downloads on their first run; hosted generation and the larger embedding comparison are disabled by default. Save student reports and tables under `local/student/2026-2027/week_1/`.

Week 2 follows text through a tokenizer, model logits, softmax and a predicted label. Students then explore masked-token prediction and GPT-2 generation, measure batching on labelled reviews, and compare DistilBERT with BERT. Timing supports CPU, CUDA/ROCm and Apple MPS. Memory measurements cover the Python process and, on CUDA/ROCm devices, PyTorch tensor allocations; MPS GPU memory is not measured.

Week 3 follows one churn-analysis task: check six rows by hand, validate API replies, generate and inspect Python, execute it, improve the plot, and reuse the checked code on 600 customers. Students compare sending all the data with generating code from six example rows. The final exercise asks them to add confidence intervals, test whether churn is associated with contract type, and write a supported conclusion. Students write their own prompts and implementation for that exercise.

## Rules of the game

- **Lecture: screens off.** Listen, ask questions, discuss, and sketch ideas on paper.
- **Lab: individual work with tools.** Use laptops, AI assistants, and coding tools. Discuss questions, but complete your own analysis, check the results, and be able to explain your work.
- **Final evaluation: one hackathon day.** Build a working product around an agent loop: the model calls tools, receives observations, and revises the work. Demonstrate what you learned by showing the product and the loop running.

## Lab setup

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter lab labs
```

Select this environment as the notebook's Python kernel. On Windows, replace the activation command with `.venv\Scripts\Activate.ps1` in PowerShell.

For hosted calls, also run `python -m pip install -r requirements-live.txt` and set the relevant API key in a local `.env` file at the repository root; [.env.example](.env.example) lists the variable names. Week 3 needs `GEMINI_API_KEY` and uses the common course model `gemini-3.5-flash-lite`. Calls use account quota and may incur charges.

### Week 3 execution settings

The Week 3 lab follows the lecture's churn analysis, from a six-row check to the full dataset. Inspected Python can run in Docker or in a separate local Python process. For Docker, start its engine and prepare the image before class:

```sh
docker build -t llm-course-eda -f labs/Dockerfile.eda .
```

The notebook includes Docker installation and startup instructions for macOS, Windows and Linux. Its current settings are:

| Setting | Current value | Meaning |
|---|---|---|
| `RUN_LIVE` | `True` | Enable hosted requests after API setup. Set `False` to use worked examples without API requests. |
| `RUN_SANDBOX` | `False` | Select a separate local Python process using the notebook's environment. Set `True` to use Docker. |
| `RUN_LOADING_CODE` | `False` | Enable only after inspecting the generated loading function. |
| `RUN_ANALYSIS_CODE` | `False` | Enable only after inspecting both loading and analysis functions. |
| `RUN_REVISED_CODE` | `False` | Enable only after inspecting the complete revision. |

The three code execution switches are off. These exercises show labelled saved examples when execution is skipped. A full-data run requires a six-row analysis that has passed the supplied checks.

Local execution has the notebook's file permissions and is not a sandbox. Docker execution restricts access and resources, with no runtime network access. A failed Docker readiness check selects local mode; it does not enable the three review switches.

**Section 6, the token and cost comparison, has no extra execution switches.** With live API setup, running its cells sends two requests: one supplies all 600 CSV rows and asks for the numerical answer; the other supplies six rows and asks for a complete Python script that reads the full CSV. The execution cell runs that script in the selected mode and checks both results. It then compares token counts and estimated API costs using the supplied course-model prices. The script and usage log are saved under `local/student/2026-2027/week3/`.

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

`main` is the current course. The branch `archive/2025-2026` preserves the previous slides and labs, including the notebook edits present before this revision.

Run `make slides` to rebuild the PDFs and `make check` for notebook checks and the agent tests. Hosted calls and Docker execution require their respective services and are separate from the offline checks.

Instructor: Sebastian Mueller · Aix-Marseille Université
