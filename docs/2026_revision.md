# Revision for 2026–2027

Sources checked on 1 October 2026. `archive/2025-2026` preserves the previous slides and labs, including the two notebook edits present when revision began. Its commit is `be98e2657c61`; parent `d6059a2`. The original science-course outline is stored locally with the instructor materials.

## Scope of the revision

Keep the original six-week order, illustrated explanations, lab tasks, and hackathon grading. The changes are:

- Update the course date and provider tables; configure API model identifiers instead of relying on old defaults.
- Migrate the Gemini examples from `google-generativeai` to `google-genai`, following [Google's migration guide](https://ai.google.dev/gemini-api/docs/migrate). Keep the existing prompting exercises.
- Correct the OpenAI classifier setup and token-limit parameter using the [Chat API reference](https://developers.openai.com/api/reference/resources/chat).
- Exclude padding from mean-pooled embeddings and respect explicit retrieval metadata filters.
- Replace the EDA cell's host `exec` with a separate, limited Docker environment. Preserve code generation, printed analysis, and plots.
- Remove the duplicate text-only embedding recap and unsupported claims of superior accuracy or prompting performance. Keep every original TikZ diagram and image reference.
- Retain the RAG material; add a full-context comparison and a short agent-loop section at the end of Week 5. Detailed retrieval experiments can be shortened for time.
- Keep the original four hackathon criteria; ask teams to support performance claims with a baseline and measured results.
- Add recent lecture/video references and ignored local directories for private teaching materials.

## Developments since the previous edition

| Development | Source | Small teaching update |
|---|---|---|
| Agent courses now treat tools, state, and evaluation together | [Google/Kaggle June 2026 course](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google) | Extend the existing Python exercise with an explicit decision/observation loop. |
| Longer tasks need persistent progress and checks | [Anthropic: effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), November 2025 | Save a trace and enforce a step budget. |
| Agent evaluation covers outcomes and trajectories | [Anthropic: demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), January 2026 | Inspect the error/revision trace and verify completion independently. |
| Managed execution reduces the environment setup students must write | [Gemini code execution](https://ai.google.dev/gemini-api/docs/code-execution) and [Anthropic managed agents](https://www.anthropic.com/engineering/managed-agents), April 2026 | Compare our visible loop with a managed alternative after understanding the mechanics. |
| Productivity evidence depends on task selection and time accounting | [METR's February 2026 update](https://metr.org/blog/2026-02-24-uplift-update/) | Count prompting, waiting, review, and repair; do not infer a universal speedup. |

These sources inform the teaching choices; they do not establish that an LLM can perform every junior data scientist's task independently.

## Retrieval remains a choice

[Google's long-context guidance](https://ai.google.dev/gemini-api/docs/long-context) describes direct document input and its remaining accuracy/latency limits. [Anthropic's context-engineering discussion](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) includes retrieval for selecting evidence. Keep the old RAG explanations and compare them with putting this small course corpus directly into context. Retrieval becomes an optional agent tool when the task warrants it.

## Local materials

Slides, reusable notebooks, and public/synthetic datasets remain shared. Private existing files were moved to `local/student/2025-2026/` and `local/instructor/2025-2026/`; current private work uses the corresponding `2026-2027/` directories. `local/` and `.env` files are ignored. No remote branch has been published.
