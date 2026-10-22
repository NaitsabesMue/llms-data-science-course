# Week 5 — revised lecture and lab

21 October 2026. The reviewed slides and revised `labs/week_5_rag.ipynb` follow
the instructor's [teaching guidance](../skills/course-lecture-review/SKILL.md).
The new notebook is ready for joint review. The previous Python-agent notebook
is retained separately, outside the core Week 5 activity.

## Main changes

The previous deck retained 26 slides from last year's retrieval lecture, then
added a full-context comparison and three agent slides. The result introduced
many search terms before their purpose and left the course's agent loop at the end.

The revised 17-slide route follows one question from Week 4: a student has lost
their card. Week 4 predicts a label; Week 5 answers the question using documents.
These are separate tasks: answering does not require a classification step.
Students first see the documents and complete prompt, then retrieval, then how
a second model call reviews the answer and sends feedback for revision.
The final section collects official AMU webpages, builds a local RAG collection,
and compares it with a model using web search. The Week 3 churn detour was removed.

Preserved and adapted:

- The three original TikZ diagrams: direct input versus retrieval, keyword and
  embedding search, and the assembled prompt. Colours remain consistent; input
  paths and feedback arrows have been checked in the rendered slides.
- The AMU student-service setting, keyword/embedding retrieval, source IDs,
  prompt construction, precision/recall and answer verification.

Removed from the main lecture:

- Repeated course recaps, duplicated diagram/list explanations, fine-tuning
  comparisons and general closing reminders.
- The BM25 formula and naming history, lists of index products, undefined
  reranking operations and a prescribed metadata-filter order.
- The cloud-execution comparison and “optional” agent section. The loop is now
  part of the main progression.

## Slide route

| Slide | Purpose |
|---|---|
| 1 | Documents, retrieval and agent loops. |
| 2 | Change the task from predicting a label to answering directly from documents. |
| 3 | Show six fictional documents covering cards, library loans, Wi-Fi and timetables; D2/D3 answer the lost-card question. |
| 4 | Show the actual full-document prompt, including the original question. |
| 5 | Define RAG and compare direct document input with selecting passages first. |
| 6 | Explain keyword and embedding search; preserve the diagram combining results. |
| 7 | Show instructions, question and selected passages entering the same prompt. |
| 8 | Keep the full student question as the search input; identify D2/D3 as the reference set and define precision/recall. |
| 9 | Check an illustrative answer against D2/D3; the missing-price question has no supporting fact. |
| 10 | Retrieve once, generate an answer, review it in a second call, and return feedback for revision. |
| 11 | Walk through the answer--review loop, with at most four attempts (eight model calls) and explicit stopping statuses. |
| 12 | Move from fictional documents to three linked official AMU sources, preserving institutional scope. |
| 13 | Download HTML, extract text, split into passages and store embeddings with URLs and dates. |
| 14 | Compare our RAG, RAG with review, and a model with web search; keep the model fixed first, then compare another. |
| 15 | Evaluate the same questions against independently checked facts and sources; report total time and cost. |
| 16 | Build and evaluate an AMU assistant in the lab. |
| 17 | Link RAG, long-context, web-search and agent teaching references. |

## Worked example and checks

The new reusable files in `slides/examples/week5_retrieval/` contain the six
fictional documents, the complete prompt and a small Python search/loop example.
They do not contain credentials or make API calls on import.

The initial model-selected search loop has been replaced by the instructor's
answer--review workflow. Retrieve passages once using the full original question.
The writer receives the question, passages, previous answer and feedback; the
reviewer receives the same question and passages plus the current answer. Both
roles can use the same model in separate calls.

`workflow.py` contains the two API functions and a bounded `run_loop`. A review
returns `accepted`, `revise`, or `missing_information`, with explanatory feedback.
Missing information stops this fixed-context loop; it means the supplied passages
are insufficient, not that the whole collection lacks the information. Four
attempts mean at most eight calls. If the last review requests revision, the
workflow reports `attempt_limit` rather than accepting the draft. Exceptions are
surfaced without hidden retries. Review acceptance remains a model judgment;
compare the final answers with independently checked source/reference answers.

Seven offline tests check prompt/corpus consistency, feedback and previous-answer
propagation, the eight-call limit, missing-information stopping, malformed review
rejection, API input evidence, and valid attempt limits. No live model requests
or generated Python were executed for this review. The slide's `retrieve` function
uses the lab retrieval implementation; multilingual embeddings are needed for
the French question and English documents.

## Points to review together

- The first nine slides cover document input and retrieval. Slide 10 shows the
  answer--review loop; slide 11 walks through it once in code. Separate slides defining a tool,
  action formats, feedback, the API wrapper and stopping repeated the same mechanism
  and have been consolidated. Full helper definitions remain in the example source.
- Stay with student-service questions throughout. The fictional D1--D6 collection
  makes the first mechanism easy to inspect; the final section explicitly replaces
  it with official AMU pages. The IUT card procedure must not be generalized to
  every faculty. Keep collection scope in the question and source metadata.
- Compare the course model in the notebook with its search-enabled free AI Studio
  interface before adding a different browser model. The second comparison measures complete systems; it does not
  isolate retrieval. Keep the same questions and answer instructions. Ask for
  official AMU sources, and inspect the returned URLs; a prompt request is not a
  technical domain filter.

## Verified sources and collection plan

`slides/examples/week5_retrieval/amu_sources.json` lists three official pages
verified on 21 October 2026: IUT student administration, DirNum Wi-Fi, and BU
borrowing/reservations. It is a source manifest, not a downloaded dataset. The
IUT page gives an actual replacement procedure via the ENT, unlike the fictional
teaching text; keep those two stages visibly distinct.

The lecture names `requests` for downloading HTML and `BeautifulSoup` for
extracting page content. Start with these selected URLs, inspect the text and
preserve headings, scope, URL and download date. Split into passages and reuse
the retrieval methods already introduced. Download once and keep the snapshot
for repeated runs. The revised notebook implements this collection step and the RAG workflow.
It downloads only the selected pages and reuses saved snapshots.

Free access was rechecked on 21 October 2026. Gemini 3.5 Flash-Lite has a free
API tier for generation, but its Search grounding API requires paid-tier access.
The lab therefore keeps full-context answers, RAG and review in the notebook
using a Free Tier project key. The search comparison takes place manually in
free AI Studio, with search enabled and without linking a paid API key. The
notebook prints the same question and answer requirements for copying.
Students save the browser answer and citations, comparing quality and sources;
browser timings remain separate and unavailable token counts are not invented.
If free browser search is unavailable, record that limitation without enabling billing.

Gemini 2.5 Flash/Flash-Lite still list free search, but Google's deprecation page
restricts 2.5 access to previous users. They are unsuitable defaults for new
students. The lab does not require billing activation or purchased credits.
Free project quotas and account eligibility still apply; no hosted call was made
to validate any particular student's quota or access.

## Notebook structure and scope

`labs/week_5_rag.ipynb` now contains 41 cells, including 20 code cells. The core
uses one worked question and three real AMU pages; allow roughly 75–90 minutes
including source reading and inspection. The API sections execute when their
cells are run, without additional flags or simulated fallback answers.

1. **Collect and inspect:** cache the selected pages, preserve headings and
   institution/service scope, inspect the card instructions, then split sections
   into passages with stable IDs, source URLs, timestamps and checksums.
2. **Retrieve:** reuse Week 4's multilingual MiniLM, send the complete original
   question, and inspect the results. Students mark a reference set before
   computing precision/recall. No reference labels are invented from rankings.
3. **Answer:** compare full-document context and retrieved context with the same
   model and instructions. Show the actual prompt and use source IDs consistently.
4. **Review:** display the two API functions and the complete answer--review loop.
   Keep the question and passages fixed; send the previous answer and feedback
   to the writer. Stop on accepted/missing-information or four attempts.
5. **Search online:** copy the printed prompt into a free AI Studio chat, enable
   Google Search, inspect the citations and save the answer locally. No paid
   search-tool request is sent by the notebook.
6. **Compare:** show latest-run records for the three notebook workflows, every
   model call, elapsed time, tokens (including thinking) and reference paid-rate
   estimates. These estimates are not free-tier bills. Compare the browser answer
   separately by quality and sources. Missing counts remain unknown.
7. **Exercise:** use a new development question, freeze settings, and write three
   test questions with independently checked reference facts and sources. Include
   a missing-information case. Students implement evaluation and conclusions.

Extensions keep a second-model comparison in free AI Studio and original BM25/hybrid
retrievers. They are separate from the core run. The earlier code-execution
notebook is preserved but no longer linked as the next required activity.

The notebook uses `labs/week5_helpers.py` for HTML extraction, caching, passage
construction and experiment records. The model calls, prompts, retrieval and
review loop stay visible. The shared requirements now include `requests` and
`beautifulsoup4`; `%pip` in the notebook installs into its active kernel.

API setup reuses the repository `.env`, `gemini-3.5-flash-lite`, a two-minute
timeout and one SDK attempt. Students select a Free Tier project in AI Studio
and leave billing disabled. A paid project key can incur charges; the notebook
cannot infer a billing plan from a key. No credentials are printed or embedded.
The core requires 4–10 requests; exercises and reruns consume additional quota.
Quota errors require waiting for the indicated reset, not paying to continue.
The second browser model is `gemini-3.8-flash`, only where available for free.

## Notebook validation

- Downloaded all three public pages successfully. Checked the IUT accordion
  extraction: its card FAQ now retains its own heading, rather than a preceding
  campus heading. Cached snapshots are checked before reuse.
- Ran every non-installation code cell with actual downloaded HTML and the cached
  multilingual embedding model. The original question retrieved the relevant
  lost-card passages. Used six explicitly mocked API replies to exercise the
  three notebook workflows, including a revision. Checked that the browser-prompt
  cells make no API calls, including the second-model extension.
- No `.env` was read during validation and no hosted model request was sent.
  Mock outputs live only in the temporary validation directory; the shared
  notebook has no saved outputs or execution counts.
- Added tests for extraction, cache integrity, failed downloads, source/ID
  preservation, retrieval metrics, unreported usage, search/thinking costs,
  latest-run accounting and notebook defaults. Existing loop tests cover feedback,
  stopping and invalid reviews. `make check` passes all 59 tests and every notebook
  passes syntax/format validation.

## Sources

- [Lewis et al., RAG](https://arxiv.org/abs/2005.11401).
- [Google, long context](https://ai.google.dev/gemini-api/docs/long-context).
- [Google, Search grounding](https://ai.google.dev/gemini-api/docs/google-search).
- [Google, billing and free AI Studio access](https://ai.google.dev/gemini-api/docs/billing).
- [Google, model availability and deprecations](https://ai.google.dev/gemini-api/docs/deprecations).
- [IUT, student administration](https://iut.univ-amu.fr/fr/services-de-scolarite).
- [DirNum, Wi-Fi](https://dirnum.univ-amu.fr/fr/reseau-fil-wifi).
- [BU, borrowing and reservations](https://bu.univ-amu.fr/fr/vos-services/emprunter-reserver-documents).
- [Anthropic, building effective agents](https://www.anthropic.com/research/building-effective-agents).
- [Hugging Face Agents Course, Unit 1](https://huggingface.co/learn/agents-course/en/unit1/introduction).

The PDF was compiled and the revised AMU collection/comparison slides rendered
and inspected.
The retained slides were visually checked in the previous revision. Content has no
overfull boxes; the shared theme's existing title-slide width warnings remain.

## Website timeout handling

The notebook now tries each website with a 5-second connection timeout and a
30-second read timeout. Request failures or unusable HTML fall back to the actual
AMU HTML collected on 21 October 2026, bundled in `slides/examples/week5_retrieval/snapshots/`.
The source URL and checksum are validated. The fallback and original failure are
reported, retained in the local cache and shown in the document-origin table.
Reusing that cache keeps the experiment stable; choosing a new directory retries
live collection. Missing or damaged bundled files still raise an error.
