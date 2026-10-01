# Videos, courses, and readings

Selected for 2026–2027; checked on 1 October 2026. Dates identify the edition or article, not an unchanged webpage. Official course hubs provide recordings and current code.

## Viewing path

| Resource | Edition / format | What to study | Session |
|---|---|---|---|
| Stanford, [CS336: Language Modeling from Scratch](https://cs336.stanford.edu/) and [official recordings](https://www.youtube.com/playlist?list=PLoROMvodv4rMqXOcazWaTUHhq-yembLCV) | Spring 2026; recorded university lectures and executable notes | Lectures 1 and 3 for tokenization and architecture; lecture 10 for inference; lecture 15 for post-training. Select excerpts rather than assign the whole course. | 1–2 |
| Stanford Online, [CS336 lecture 1: Overview and Tokenization](https://www.youtube.com/watch?v=SQ3fZ1sAqXI) | 24 April 2025 upload; full lecture video | A direct video companion for the first lab. | 1 |
| Google/Kaggle, [5-Day AI Agents: Intensive Vibe Coding Course](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google) | 15–19 June 2026; livestreams and recordings | Specifications, tools, state, evaluation, observability. Start with this recent edition and follow the official page to recordings. | 5–6 |
| Andrew Ng, [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai) | Current video course; catalogue checked October 2026 | Task decomposition and evaluation in module 1, then reflection, tool use, planning. The catalogue lists 31 lessons; certificate/graded access is separate. | 5–6 |
| Google/Kaggle, [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents) | 10–14 November 2025; recorded course and notebooks | Introduction; tools; sessions and memory; quality. A fuller companion to the 2026 edition. | 5–6 |
| Google/Kaggle, [Day 3: Context Engineering, Sessions and Memory](https://www.youtube.com/watch?v=8o-GXj8A3nE) | November 2025 livestream | How state and retrieved context affect the next action. Also linked by [speaker Julia Wiesinger](https://www.linkedin.com/posts/julia-wiesinger_agents-contextengineering-developertools-activity-7394736952488583168-N9FU). | 5–6 |
| Hugging Face, [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) | Living course launched in 2025; lessons, code, live-session links | Unit 1: action/observation cycle; unit 2: frameworks; unit 3: agentic retrieval. | 5–6 |

Preparation follows the course order: selected Stanford 2026 lectures for sessions 1–2, then the original prompting and classification labs, followed by Andrew Ng's decomposition/evaluation lessons, Hugging Face's [agent cycle](https://huggingface.co/learn/agents-course/en/unit1/introduction), and the context/memory livestream. Identify one task, tool, observation, and stopping condition. Full courses are optional.

Course hubs were checked; individual YouTube playback was not verified in this environment.

## Class readings

| Reading | Date | Purpose |
|---|---|---|
| Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 29 September 2025 | Selecting context and keeping state over a long task. |
| Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 26 November 2025 | Progress records and tests across sessions. |
| Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 9 January 2026 | Tasks, trials, traces, graders; project evaluation design. |
| Anthropic, [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) | 8 April 2026 | Model, loop, execution environment. |
| METR, [Changing the developer productivity experiment](https://metr.org/blog/2026-02-24-uplift-update/) | 24 February 2026 | Task selection and time accounting. Developer evidence, not a data-scientist role benchmark. |
| [Google GenAI SDK migration](https://ai.google.dev/gemini-api/docs/migrate) | Living documentation | Replacement for the previous labs' legacy SDK. |

## Foundations and optional implementation

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017. Transformer foundation, rather than a recent development.
- [Transformers documentation](https://huggingface.co/docs/transformers/en/index): core lab reference for tokenization, model loading, generation, and revisions.
- [Google long-context guidance](https://ai.google.dev/gemini-api/docs/long-context): compare direct document context with retrieval and check accuracy/latency limits.
- [Google ADK documentation](https://google.github.io/adk-docs/): optional implementation after the small Python loop.
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro): tool interoperability; distinguish it from the control loop.

- [Gemini code execution](https://ai.google.dev/gemini-api/docs/code-execution): a provider-managed Python tool; compare its trace and checks with the course loop.
- [Claude code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool): provider-managed execution with files and results.
- [E2B code interpreter](https://github.com/e2b-dev/code-interpreter): a separate execution service usable with different model providers.
- [Docker run reference](https://docs.docker.com/engine/containers/run/): execution limits used in the local lab.
