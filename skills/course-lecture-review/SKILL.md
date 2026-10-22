---
name: course-lecture-review
description: Revise or review this repository's LLM data-science lectures and labs using the instructor's established teaching style, terminology and level of detail.
---

# Revise this course

Use the jointly revised Weeks 1–4 as the teaching reference. The audience knows
Python, statistics and basic machine learning, but is encountering many LLM tools
and terms for the first time. The purpose is to improve students' data-science
work through models, execution, feedback and independent quality checks.

## Preserve the teaching route

- Stay close to last year's useful structure, tasks and illustrations. Replace
  outdated material and remove duplication; do not replace the course wholesale.
- Check the archive before describing a method as new or changed. A short lecture
  briefing and a detailed lab may intentionally explain the same method differently.
- Keep foundations: tokens, embeddings, prediction, attention, training and
  inference. Arrive at agent loops through examples of work students can perform.
- Begin a session with a concrete question and connect it to the previous week.
  Introduce the task, input and expected output before the machinery.
- Follow one example through successive steps. Keep the same text, dataset,
  labels, variable names and conventions unless a change has a stated purpose.
- Give each slide one teaching purpose. Its conclusion should make the next
  question natural. Merge duplicate explanations; split dense slides instead of
  shrinking text. Preserve the main picture when introducing a component.
- Keep classification and evaluation as the quality-control thread for later
  retrieval and agent workflows. RAG is selected evidence supplied to generation;
  compare it with full-document context when appropriate. It can be an agent tool.

## Explain before abbreviating

- Use standard scientific terminology and conventional notation. Do not invent
  replacement terms such as "learned offset" for a bias. Explain new terms and
  symbols at first use, including their input, output and purpose.
- Use one name consistently for each concept. Do not alternate near-synonyms as
  if they were new concepts; explain distinctions only when the example needs them.
- Use the method's familiar name as its slide title. Keep the established task
  vocabulary: in classification, say "correct label", not "correct route".
  Do not respond to confusion by introducing another name or acronym.
- When asked to simplify, first remove unnecessary terms or detail. Do not add
  a terminology detour to justify a confusing label or an avoidable distinction.
- Show what is actually calculated, what changes and what stays fixed. Give
  dimensions or counts when they make an otherwise abstract operation concrete.
- Teach the conceptual mechanism before implementation details. Do not insert
  embedding lookup, matrix arithmetic, API options or architecture variants merely
  because they are technically available. Add a formula when it answers the
  students' current question; define every symbol it introduces.
- Once a table or example explains a relationship, remove a second explanation
  of the same relationship. In Week 4, the label/description table made the
  dictionary-lookup diagram redundant; that space was used to explain the model.
- Explain code constructs beside their first appearance when needed to follow
  the example: dictionary unpacking, result indexing, evaluation mode, generation
  settings and returned text. State which variables are ordinary Python strings
  and which names are API fields. Distinguish code generation from code execution.
- Separate architecture from similarly named software; pretrained model from
  task-specific training; prompt context from parameter updates; and attention
  weights from a padding mask.

## Make the explanation visible

- Prefer a worked diagram, before/after representation, actual output, plot or
  short code path to an abstract list of capabilities or recommendations.
- Preserve existing figures. Improve spacing, legibility and explanatory arrows.
  Diagrams must show where context comes from and where it enters the calculation.
  Check each arrow's direction and meaning in the rendered result. Distinguish
  data inputs, model candidates and feedback rather than using one ambiguous flow.
- Use examples to connect architecture with application: relevant context matters;
  sampling changes variability; plausible output still needs verification.
  Do not imply hallucinations are caused only by sampling or attention.
- See [specific lessons](references/lessons.md) for attention, probabilities,
  uncertainty, execution and experiment-design pitfalls encountered in this course.

## Formulate claims precisely

- Write direct, natural sentences. Remove hype, canned motivation, metaphors such
  as "chatbot brain" and "showdown", and repetitive lists. Do not bold a term
  simply because the instructor asked about it.
- Remove routine closing sentences from slides: generic reminders, caveats,
  summaries and unsolicited contrasts are AI slop in this lecture style.
  Example to remove: "Prompting does not update model weights." Check every
  slide ending; retain it only if it adds an explanation needed for that slide's
  teaching purpose. Do not replace a deleted ending with another takeaway.
- Explain practical stakes through tasks, decisions and consequences. Do not turn
  claims about replacing junior work or society into unsupported predictions.
- Do not announce a best method before evaluating it. Distinguish model scores,
  correctness, calibration, statistical uncertainty and causal conclusions.
- Verify changing model availability, API behavior and current-event claims using
  primary sources. Attribute company-reported results. Never invent future model
  releases or present illustrative numbers as measured results.
- Cite an explanation or lecture where useful. Learn from clear explainers while
  keeping attribution and avoiding unlicensed copying of their visuals.

## Align the lab with the lecture

- Reuse the lecture's example and sequence. Students should predict, run, inspect,
  change something meaningful, verify it and justify a decision.
- Show real returned code and results where available. Repair from actual errors
  or a concrete improvement request. Label any deliberately introduced fault and
  every saved/offline example; do not fabricate a failure narrative.
- Make improvement concrete: show a missed case, the proposed change and its
  effects. An LLM can suggest regex changes or generate synthetic debugging data;
  students inspect the suggestion and labels, then compare on development cases.
- Provide runnable demonstrations, then leave genuinely open exercises for
  students. When the instructor requests an exercise without a solution, remove
  the solution and scaffolding that already performs it.
- Keep execution linear and rerunnable. Avoid unnecessary flags and opaque helper
  layers. Preserve explicitly requested code-review switches, initially off.
  Document exceptions, such as a comparison cell that executes directly.
- Labs are individual work with tools and discussion permitted. Do not introduce
  partners, submissions or extra deliverables. The final assessment remains the
  separately specified hackathon: a working product using a checked agent loop.
- Use one shared course API model where specified. Keep keys local. Make local
  execution and Docker choices clear without introducing a new provider by default.

## Review and deliver

Read the existing deck and corresponding notebook before revising. Check the
sequence, undefined terms, repeated material, unsupported claims, output examples
and exercise fit. Distinguish changes made from recommendations still pending.
For a first pass, retain the core task and methods and record open decisions in
`docs/week_N_review.md` so the instructor can review slides in order.
Keep measurement explanations proportional to the task. For Week 4, measure
time to obtain a label after loading/training, and API tokens; a method-by-method
timing breakdown and an empty slide table to fill in were rejected. Put computed
results in the notebook. Introduce the next week through one concrete continuation
of the current example, with any change in the task stated explicitly.

Build changed LaTeX decks and inspect rendered slides, especially diagrams, tables
and code. Check for clipping and illegible text; a successful build is insufficient.
Validate notebook format and relevant code paths without sending paid API requests
or executing generated local code just to review prose. Match README instructions
to actual defaults and revised material status. Do not publish or push unless asked.

Reusable slides, notebooks and public/synthetic data stay in Git. Private work,
solutions, grades, traces and instructor notes stay under ignored `local/` paths.
Last year's materials are preserved in `archive/2025-2026`; do not overwrite them.
