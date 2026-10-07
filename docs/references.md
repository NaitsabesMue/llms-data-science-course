# Videos, courses, and readings

Selected for 2026–2027; updated on 2 October 2026. Dates identify the edition or article, not an unchanged webpage. Official course hubs provide recordings and current code.

## Viewing path

| Resource | Edition / format | What to study | Session |
|---|---|---|---|
| Stanford, [CS336: Language Modeling from Scratch](https://cs336.stanford.edu/) | Spring 2026; lecture materials and executable notes | Lecture 1 for tokenization and lecture 3 for architecture. Use the current course schedule; select excerpts rather than assign the whole course. | 1–2 |
| Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | 2018 illustrated explanation | Follow one block; connect the diagrams to the worked attention example. Retained for the foundations. | 1 |
| Georgia Tech Polo Club, [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) | Interactive visualisation; living site | Change the prompt and trace attention, token scores, and generation. | 1 |
| Josh Starmer, [Attention in Transformers: Concepts and Code in PyTorch](https://www.deeplearning.ai/courses/attention-in-transformers-concepts-and-code-in-pytorch) | Video course; catalogue checked October 2026 | Main ideas, self-attention calculation, masking, and code. The catalogue lists 11 lessons and 3 code examples; this is not a newly released 2026 course. | 1 |
| Jay Alammar and Maarten Grootendorst, [How Transformer LLMs Work](https://www.deeplearning.ai/courses/how-transformer-llms-work) | DeepLearning.AI video course; catalogue checked October 2026 | Self-Attention (10 min) and The Transformer Block (6 min): companions to the attention and residual-connection walkthrough. | 1 |
| Grant Sanderson, [Attention in transformers, step-by-step](https://www.3blue1brown.com/lessons/attention/) | 7 April 2024; animation and illustrated transcript | Context changes the representation of a token; values form an attention contribution which is added to the original representation. The transcript explicitly distinguishes the weighted sum from this addition. | 1 |
| Stanford Online, [CS336 lecture 1: Overview and Tokenization](https://www.youtube.com/watch?v=SQ3fZ1sAqXI) | 24 April 2025 upload; full lecture video | A direct video companion for the first lab. | 1 |
| Google/Kaggle, [5-Day AI Agents: Intensive Vibe Coding Course](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google) | 15–19 June 2026; livestreams and recordings | Specifications, tools, state, evaluation, observability. Start with this recent edition and follow the official page to recordings. | 5–6 |
| Andrew Ng, [Agentic AI](https://www.deeplearning.ai/courses/agentic-ai) | Current video course; catalogue checked October 2026 | Task decomposition and evaluation in module 1, then reflection, tool use, planning. The catalogue lists 31 lessons; certificate/graded access is separate. | 5–6 |
| Google/Kaggle, [5-Day AI Agents Intensive](https://www.kaggle.com/learn-guide/5-day-agents) | 10–14 November 2025; recorded course and notebooks | Introduction; tools; sessions and memory; quality. A fuller companion to the 2026 edition. | 5–6 |
| Google/Kaggle, [Day 3: Context Engineering, Sessions and Memory](https://www.youtube.com/watch?v=8o-GXj8A3nE) | November 2025 livestream | How state and retrieved context affect the next action. Also linked by [speaker Julia Wiesinger](https://www.linkedin.com/posts/julia-wiesinger_agents-contextengineering-developertools-activity-7394736952488583168-N9FU). | 5–6 |
| Hugging Face, [Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction) | Living course launched in 2025; lessons, code, live-session links | Unit 1: action/observation cycle; unit 2: frameworks; unit 3: agentic retrieval. | 5–6 |

Preparation follows the course order: selected Stanford 2026 lectures for sessions 1–2, then the original prompting and classification labs, followed by Andrew Ng's decomposition/evaluation lessons, Hugging Face's [agent cycle](https://huggingface.co/learn/agents-course/en/unit1/introduction), and the context/memory livestream. Identify one task, tool, observation, and stopping condition. Full courses are optional.

Course hubs were checked; individual YouTube playback was not verified in this environment.

## Week 1: attention teaching sequence and video choices

The lecture and [offline animation](../visualizations/attention/index.html) use **red toy robot** throughout. The animation can be played or stepped manually. Its optional matrix view highlights an input row, a matrix column, and the successive products forming the selected result. Open the HTML file in a browser; keep its CSS and JavaScript files alongside it. No server or network is required.

The sequence follows [3Blue1Brown's attention lesson](https://www.3blue1brown.com/lessons/attention/): establish the contextual change we want before explaining how queries, keys, values and addition produce it. The diagrams and implementation are original; they do not reproduce video clips or screenshots.

1. **Purpose.** The representation at `robot` should incorporate context from `red` and `toy`: `toy` specifies a plaything, changing the kind of object. The word remains `robot`; we change its numerical representation. The geometric picture is schematic, not a measured embedding plot.
2. **Three learned transformations.** The same incoming representations produce queries, keys and values. The trained matrices stay fixed during inference; the resulting vectors depend on the input. Optional opening: Starmer's **The Main Ideas Behind Transformers and Attention** (4 min), or Alammar/Grootendorst's **Self-Attention** (10 min).
3. **One comparison, then all comparisons.** Follow `robot`'s query against the `toy` key, coordinate by coordinate. Then put all query/key comparisons into `Q Kᵀ`. The transpose turns key rows into columns. Starmer's **The Matrix Math for Calculating Self-Attention** (11 min) is a numerical companion.
4. **Allowed context and weights.** A causal decoder excludes future positions before row-wise softmax. Each position gets its own weights. `robot` can use all three tokens; `toy` cannot use later `robot`. Starmer's **Self-Attention vs Masked Self-Attention** (14 min) is an optional follow-up.
5. **Information to pass.** The attention weights combine value vectors. `A V` calculates every position's attention contribution. A mixing coefficient is not a percentage of retained meaning or a next-token probability.
6. **Add context.** The original representation has a direct residual path and is added to the attention contribution. [The original paper, Section 3.1](https://arxiv.org/html/1706.03762v7) distinguishes attention computation, residual addition and normalisation. The lecture labels omitted operations explicitly.
7. **Complete the block, then compare again.** Feed-forward processing acts separately at each position and also has a residual addition. The next block receives the richer representations and calculates new queries, keys and values with its own learned matrices. Alammar/Grootendorst's **The Transformer Block** (6 min) and [Alammar's residual diagrams](https://jalammar.github.io/illustrated-transformer/#the-residuals) are companions. An updated query is never matched against the old keys halfway through the current attention calculation.
8. **Generate.** After the final decoder block, the output layer gives next-token probabilities. Choose and append a token, then repeat. These generation steps are different from the stacked blocks within a single model pass. Starmer's **Encoder-Decoder Attention** (4 min) accompanies the translation extension.

DeepLearning.AI lesson titles and approximate durations were checked against the official course catalogues: [Starmer](https://www.deeplearning.ai/courses/attention-in-transformers-concepts-and-code-in-pytorch), [Alammar/Grootendorst](https://www.deeplearning.ai/courses/how-transformer-llms-work). Course playback may require signing in; lesson playback and timestamps were not verified here.

### Shared numerical example

Rows represent `red`, `toy`, `robot`, in that order. Input representations `X = I₃` are chosen for easy arithmetic, not extracted from a trained model. The learned query and key maps are illustrated by `WQ = [[1,0],[0,1],[1,1]]` and `WK = [[2,0],[0,2.3],[0,0.2]]`. Value and output maps are identity. Queries/keys have two coordinates, so scale scores by `√2`.

`robot` query `[1,1]` compared with keys `[2,0]`, `[0,2.3]`, `[0,0.2]` gives scores `[2,2.3,0.2]`. Scaled scores are approximately `[1.414214,1.626346,0.141421]`. Row softmax gives `[0.397399468,0.491309377,0.111291155]`. Its attention contribution is the weighted sum of value vectors `[1,0,0]`, `[0,1,0]`, `[0,0,1]`, yielding `[0.397399468,0.491309377,0.111291155]`. Adding its original `[0,0,1]` gives `[0.397399468,0.491309377,1.111291155]` before the remaining block operations.

The full masked attention matrix is `[[1,0,0],[0.164331593,0.835668407,0],[0.397399468,0.491309377,0.111291155]]`. Every row sums to one; future entries are zero. Numbers on slides are rounded. The example uses one head and omits normalisation and positional encoding. Real models use learned value/output projections, typically multiple heads, and normalisation. The final attention addition is not the output of the complete block.

## Week 1: from architecture to practice

The bridge after decoding turns mechanisms into application choices:

- **Context changes representations:** supply the task and relevant evidence, including units, definitions, and constraints. The `red toy robot` example shows why one contextual word can change the interpretation. Attention incorporates supplied information; it does not create missing evidence.
- **Context is finite:** select what the next model call needs, including current tool observations and progress. [Anthropic's context-engineering guidance](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) discusses curating context across agent turns. This supports the course's practical advice; longer input alone is not a quality guarantee.
- **Sampling creates variation:** [Hugging Face's generation guide](https://huggingface.co/docs/transformers/main/en/generation_strategies) distinguishes random sampling from greedy token selection. Record settings and repeat representative tasks.
- **Probability does not verify truth:** check sources, calculations, and executed results. [Kalai et al., Why Language Models Hallucinate](https://arxiv.org/abs/2509.04664), 4 September 2025, analyses statistical errors and training/evaluation incentives; its explanation does not depend on Transformer architecture alone. Treating hallucinations as a consequence of randomness alone would be misleading. A deterministic continuation can still select an incorrect claim.

These are practical consequences of the mechanisms and training behaviour, not a claim that the simplified attention matrices prove application reliability. Temperature changes token selection, not factual verification.

## Week 1 lab: tokenizer, embeddings, and inference references

Checked on 2 October 2026. The lab keeps its original robot/drone sentences, AG News sample, bag-of-words exercise, token-colour display, count histogram, and MiniLM neighbour comparison.

- [Hugging Face tokenization algorithms](https://huggingface.co/docs/transformers/main/en/tokenizer_summary): BPE and WordPiece, token pieces, and added special tokens. Count the same texts without special tokens for the tokenizer comparison.
- [Qwen3.5-0.8B model card](https://huggingface.co/Qwen/Qwen3.5-0.8B): the current-model tokenizer comparison loads tokenizer files only. Its stored chat template shows message-format overhead; no model weights or generation are involved.
- [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): the retained small model's sentence embeddings use mask-aware mean pooling and normalisation. The notebook's explicit 256-token cap follows this model's documented sentence-embedding limit. Lookup vectors and final contextual vectors are compared separately.
- [Qwen3-Embedding-0.6B model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B): optional newer multilingual comparison. Its pooling differs from MiniLM's; the notebook uses the model's SentenceTransformer configuration. Retrieval queries require the model's documented instruction format. No leaderboard rank or universal improvement is claimed.
- [Inference Providers chat completion](https://huggingface.co/docs/inference-providers/tasks/chat-completion) and [provider setup](https://huggingface.co/docs/inference-providers/index): configure the served model, provider, and token permissions. The optional cell uses `InferenceClient.chat.completions.create`; it does not assume that every Hub model is served, or that calls are free.

The optional NumPy attention exercise uses the same invented matrices as the lecture animation, with a causal mask before softmax and an explicit residual addition. It requires neither a downloaded model nor a hosted API. Token counts, vector dimensions, neighbour rankings, and generation settings are observations to record, rather than proxies for a model's overall quality.

## Model timeline: release sources

The original architecture timeline remains in Week 1. Its continuation samples releases and announcements from 2024 through **2 October 2026**. It is not an exhaustive catalogue or a ranking. Dates refer to the specific named release; previews and restricted rollouts are labelled.

| Event | Date | Primary source / availability at the event |
|---|---|---|
| GPT-4o; o1-preview | 13 May; 12 September 2024 | [OpenAI API changelog](https://developers.openai.com/api/docs/changelog), API release / preview respectively. |
| Claude 3.5 Sonnet | 20 June 2024 | [Anthropic announcement](https://www.anthropic.com/news/claude-3-5-sonnet). |
| Llama 3.1 | 23 July 2024 | [Meta announcement](https://ai.meta.com/blog/meta-llama-3-1/), downloadable weights. |
| DeepSeek-R1 | 20 January 2025 | [DeepSeek changelog](https://api-docs.deepseek.com/updates/). |
| Llama 4; Qwen3 | April 2025 | [Meta announcement](https://ai.meta.com/blog/llama-4-multimodal-intelligence/); [Qwen team's repository](https://github.com/QwenLM/Qwen3) records 29 April for Qwen3. |
| GPT-5 | 7 August 2025 | [OpenAI API changelog](https://developers.openai.com/api/docs/changelog). |
| Gemini 3 Pro | 18 November 2025 | [Google developer announcement](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-3-developers/), preview. |
| Claude Fable 5.1 / Mythos 5.1 | 1 September 2026 | [Anthropic release](https://www.anthropic.com/claude-fable-and-mythos-5-1): same underlying model, different safeguards; Fable generally available, Mythos through vetted programs. |
| GPT-6 Astra | 3 September 2026 | [OpenAI API changelog](https://developers.openai.com/api/docs/changelog), API release. |
| DeepSeek V4.1 Flash | 10 September 2026 | [DeepSeek changelog](https://api-docs.deepseek.com/updates/), native multimodal API release. |
| Claude Opus 5.5 | 22 September 2026 | [Anthropic announcement](https://www.anthropic.com/claude-opus-5-5). |
| Claude Sonnet 5.5 | 28 September 2026 | [Anthropic announcement](https://www.anthropic.com/claude-sonnet-5-5). |
| GPT-6.1 Sol | 29 September 2026 | [OpenAI API changelog](https://developers.openai.com/api/docs/changelog), API release. |
| Gemini 4 Argon | 30 September 2026 | [Google announcement](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/): restricted rollout to trusted cyber defenders; broader access planned. Do not treat it as a generally available classroom API. |

The 2026 column samples recent September events, rather than every release during the year. Earlier releases include GPT-5.4 (5 March), GPT-5.5 (24 April), and GPT-5.6 (9 July), recorded in the OpenAI changelog. GPT-6 Sol and Luna followed on 22 September.

## Model access: examples behind the timeline

Checked on 2 October 2026. These examples show how availability depends on the model, safeguards, task, user, and organization.

| Event / policy | Date | Source and distinction |
|---|---|---|
| Fable 5 / Mythos 5 access suspended | 12 June 2026 | [Anthropic statement](https://www.anthropic.com/news/fable-mythos-access): an export-control directive excluded foreign nationals, inside or outside the US. Anthropic suspended both models for everyone because it could not verify nationality immediately. This was about version 5, not a current citizenship requirement for Fable 5.1. |
| Controls lifted and models redeployed | 30 June / 1 July 2026 | [Anthropic restoration](https://www.anthropic.com/news/redeploying-fable-5): Fable 5 restored globally; Mythos restored to a set of US organizations with approval. |
| Fable 5.1 / Mythos 5.1 | 1 September 2026 | [Release](https://www.anthropic.com/claude-fable-and-mythos-5-1): generally available Fable has stronger cyber/biology safeguards. Mythos access is vetted; the initial announcement limited it to a set of US organizations. |
| Life Sciences Verification Program | 17 September 2026 | [Program announcement](https://www.anthropic.com/news/life-sciences-verification-program): beta for teams/institutions, including academic labs; checks research credentials, security, and oversight. Standard and High-risk grants differ. Additional vetting remains for high-risk Mythos use. Do not infer that only registered companies can participate. |
| OpenAI hardware-key announcement | 10 August 2026 | [Daybreak announcement](https://openai.com/index/expanding-daybreak-as-the-cyber-defense-window-narrows/): individual hardware-key requirements beginning 1 September. Identity checks, approved uses, and access tiers already applied. |
| Existing individual Daybreak users' deadline | 1 October 2026 | [Current access policy](https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview): eligible paid plan, Advanced Account Security, at least one compatible physical FIDO2 security key, and identity verification. The key authenticates the account; it is not compute hardware. Passing verification does not guarantee access. |
| Daybreak specialist models | Current policy | [Official OpenAI documentation](https://learn.chatgpt.com/docs/cyber-safety): Blue approval does not grant Red or specialist-model access. The [access policy](https://help.openai.com/en/articles/20001258-openai-daybreak-trusted-access-for-cyber-overview) limits current Red applications to approved business/enterprise organizations, with some individual exceptions and additional approval for some models. |

The 1 October date is a compliance deadline in the current policy, not the date of the original hardware-key announcement. We did not establish a separate 1 October announcement. “KYC” is shorthand here for identity verification; the sources also describe account security and organizational approval, which are separate checks. No blanket US-citizenship requirement for current general-purpose Fable or GPT access is claimed.

For the course, treat continuity of access as part of workflow design: keep model choice configurable and evaluation reproducible. This is our practical conclusion from the examples, not a provider policy.

## Class readings

| Reading | Date | Purpose |
|---|---|---|
| Anthropic, [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 29 September 2025 | Selecting context and keeping state over a long task. |
| Anthropic, [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 26 November 2025 | Progress records and tests across sessions. |
| Anthropic, [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 9 January 2026 | Tasks, trials, traces, graders; project evaluation design. |
| Anthropic, [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 24 March 2026 | Examples of planning, tool execution, progress records, and checks over complete tasks. |
| Anthropic, [Mitigating the risk of prompt injections in browser use](https://www.anthropic.com/news/prompt-injection-defenses) | 24 November 2025 | Untrusted content can redirect an agent; why permissions need enforcement outside the prompt. |
| Anthropic, [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) | 8 April 2026 | Model, loop, execution environment. |
| METR, [Changing the developer productivity experiment](https://metr.org/blog/2026-02-24-uplift-update/) | 24 February 2026 | Task selection and time accounting. Developer evidence, not a data-scientist role benchmark. |
| [Google GenAI SDK migration](https://ai.google.dev/gemini-api/docs/migrate) | Living documentation | Replacement for the previous labs' legacy SDK. |

## Work, data science, and society

Added and checked on 2 October 2026 for the Week 1 framing.

| Source | Type of evidence | Lecture use |
|---|---|---|
| Brynjolfsson, Chandar, and Chen, [Canaries in the Coal Mine?](https://digitaleconomy.stanford.edu/publication/canaries-in-the-coal-mine-six-facts-about-the-recent-employment-effects-of-artificial-intelligence/), revised August 2026 | Descriptive U.S. payroll analysis through June 2026 | Early-career employment and hiring pressure in AI-exposed occupations. |
| World Economic Forum, [Future of Jobs Report 2025: Jobs outlook](https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/2-jobs-outlook/) | Employer expectations for 2025–2030, across multiple macrotrends | Big-data and AI roles are among those expected to grow fastest. Expectations are not observed job creation. |
| OECD, [AI and skills: What we know so far](https://www.oecd.org/en/publications/ai-and-skills_f843b352-en/full-report.html), 5 June 2026 | Synthesis of employer/worker surveys and policy evidence | Data interpretation, training, adoption barriers, working conditions, and accountability. Some underlying surveys predate 2026. |
| Gmyrek, Viollaz, and Winkler, [Disruption without dividend?](https://www.ilo.org/publications/disruption-without-dividend-how-digital-divide-and-task-differences-split), ILO–World Bank, 17 March 2026 | Exposure, task-composition, and connectivity analysis across 135 countries | Digital infrastructure can prevent workers from accessing potential gains; impacts differ across countries and tasks. |

The Stanford estimate is about 19% below a comparison trajectory for workers aged 22–25 in AI-exposed occupations. It is descriptive; the authors report no economy-wide displacement. It is not an estimate for French data scientists. The lecture's warning about relying on routine manual work is a teaching judgment.

The three organisational scenarios—expand, compress, reorganise—and the society questions—access, distribution, control—are our framing for discussion. They can coexist. They do not supply a numerical job forecast. Task exposure, employer intentions, and observed employment require different interpretations.

## Foundations and optional implementation

Week 1's workflow examples use these implementation sources:

- [Hugging Face: the action–observation cycle](https://huggingface.co/learn/agents-course/en/unit1/agent-steps-and-structure): how tools and their results feed the next model decision.
- [Colab Enterprise Data Science Agent](https://docs.cloud.google.com/colab/docs/use-data-science-agent): documented support for exploratory analysis, generated notebooks, predictions, and forecasts.
- [Google Cloud data agents, June 2026](https://cloud.google.com/blog/products/data-analytics/new-data-agents-across-the-agentic-data-cloud/): examples across data pipelines, modelling, dashboards, database monitoring, and scheduled actions. Features have different availability; product examples do not establish universal workflow reliability.

- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017. Transformer foundation, rather than a recent development.
- [Transformers documentation](https://huggingface.co/docs/transformers/en/index): core lab reference for tokenization, model loading, generation, and revisions.
- [Google long-context guidance](https://ai.google.dev/gemini-api/docs/long-context): compare direct document context with retrieval and check accuracy/latency limits.
- [Google ADK documentation](https://google.github.io/adk-docs/): optional implementation after the small Python loop.
- [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro): tool interoperability; distinguish it from the control loop.

- [Gemini code execution](https://ai.google.dev/gemini-api/docs/code-execution): a provider-managed Python tool; compare its trace and checks with the course loop.
- [Claude code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool): provider-managed execution with files and results.
- [E2B code interpreter](https://github.com/e2b-dev/code-interpreter): a separate execution service usable with different model providers.
- [Docker run reference](https://docs.docker.com/engine/containers/run/): execution limits used in the local lab.
