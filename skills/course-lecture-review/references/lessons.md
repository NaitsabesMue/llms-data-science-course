# Specific lessons from Weeks 1–4

These examples clarify decisions; they are not a requirement to reteach every
topic or include every formula in subsequent weeks.

## Context and attention

Follow one phrase such as **red toy robot** through the explanation. Make clear
that attention updates a vector at an existing token position; it does not replace
the input token or generate the next one. Context is other available input
representations. Introduce attention and self-attention before using those names
inside a Transformer diagram. Explain a query as the learned comparison used by a
position, keys as what it is compared with, and values as the information combined.
Queries, keys and values in one layer are computed from that layer's input; a
context update affects the next layer's projections, not the same layer's query
retroactively. Respect causal masking in a next-token example.

Attention weights describe a weighted sum of value vectors, not percentages of a
word's meaning. A residual connection also preserves an input path. Distinguish
the attention contribution from the complete block output. Introduce encoder,
decoder and encoder–decoder architecture before contrasting their roles; a
Transformer block is not an encoder–decoder pair. Remove redundant architecture
detours when the input-to-prediction route is already clear.

## Scores, randomness and verification

Logits are unnormalized class scores. Softmax turns scores into a probability
vector; this alone does not establish calibration. A well-calibrated predicted
probability of 0.8 means about 80% correct among comparable cases assigned that
probability, not 80 identical deterministic reruns out of 100. Training with a
probabilistic loss does not guarantee calibration on new inputs.

Greedy decoding chooses the highest-scoring next token. Temperature affects
sampling; changing it while sampling is disabled does not change that selection.
Explain each generation setting through an observable change. GPT-2 continues
text; it was not trained as an instruction-following chat assistant. Newlines in
the generated continuation are output text, not necessarily a display bug.

## Reproducible work and execution

An API returns text or structured content. A Python program must parse a returned
table or JSON and check its values. A valid schema does not establish correct
numbers. Show a small returned object and explain the checks separately.

Generating Python does not execute it. Start with inspected loading and analysis
functions on six known rows, then reuse checked code on the full dataset. A plot
revision can be meaningful even when the numbers are already correct. The model
can later review an actual saved plot and supply feedback for another call.

A virtual environment selects Python packages. Docker packages an application
and its environment, using the host kernel or a Linux VM on desktop systems.
Specific restrictions can make a container useful for limiting generated code;
the word "container" alone does not establish security. A separate local Python
process with a timeout is not a security sandbox. Explain permissions and the
chosen execution mode plainly. Do not silently call local execution isolated.

For the full-data/code comparison, both routes must solve the same task:

- Send every row and request the numerical answer.
- Send six example rows and request a complete script that reads the actual CSV
  path and processes every row. Do not supply a hidden preloaded DataFrame.

Check both answers, then compare request/reply usage and cost. Keep unrelated
demonstration calls out of that comparison table. Record failures and retries.
Do not multiply projected reuse cost without stating what is actually reused.

## Evaluation and statistical conclusions

Use the same labelled cases, allowed outputs and failure policy for all compared
methods. Use development cases to change rules, prompts, examples or settings;
reserve an untouched test set for final comparison. Keep related paraphrases
together when splitting. API failures and invalid outputs must not disappear
from the accuracy denominator. A hybrid or agent also needs evaluation as a
complete workflow; an added model call is not automatically an improvement.

Distinguish method from use setting. In Week 4, compare an NLI classifier that
scores request–description pairs with a generative LLM that produces a label.
Both can be used zero-shot. Label definitions alone are not labelled example
requests; adding a few such examples gives few-shot prompting. Do not present
“zero-shot” and “prompted LLM” as mutually exclusive model families.

Keep label codes and natural-language descriptions visibly paired. A description
such as “Read student email” represents the existing `check_email` label, not a
new intent. Reuse the same descriptions across examples. The notebook needs the
fixed dictionary lookup, but the instructor removed its redundant slide diagram
once the table explained the pairing. Do not imply that another model must infer
this mapping. The accepted method title is "Pretrained Classifier"; NLI internals
stay in speaker notes unless needed for a specific question.

Week 4's accepted improvement example is the regex that matches `email` but
misses `e-mail`. Ask an LLM for a revision, inspect the optional hyphen in
`e-?mail`, then count corrected predictions and new errors. This replaced an
unclear conflict involving `horaires`. The next exercise asks an LLM for ten
synthetic requests, two per existing label; students review their meaning and
labels before adding them to development data.

The accepted transition to Week 5 uses a lost-student-card question. Week 4
predicts `get_student_card`; Week 5 finds the replacement instructions and uses
them to answer the question. Define context as the supplied passage. Explain a
loop through the next action after a search result, rather than an abstract list
of missing information, tools and policies. Keep classification and answering
as explicitly different tasks when choosing evaluation cases and checks.

Intervals estimate population quantities under stated sampling assumptions;
the observed rate in a fixed dataset is already known. Let students justify an
appropriate proportion interval instead of mandating Wilson without a reason.
A confidence interval obtained by inverting a two-sided test contains exactly
the null parameter values that corresponding test does not reject. Thus a matched
95% interval for a difference excludes zero when the 5% test rejects equality.
Separate groupwise intervals are different: overlap can coexist with rejection.
An overall three-group test does not identify each differing pair. Keep effect
size, statistical evidence and causation distinct.

Timing must state what is included: model execution, preprocessing, network,
startup, warm-up, review or repair. Accelerators may execute asynchronously;
synchronization waits until submitted work completes. A larger batch need not
increase throughput. Process RSS includes the whole Python process, not just
weights. Do not treat sampled process memory or CUDA tensor allocation as an
MPS GPU peak measurement.

## Existing references

The accepted examples live in `slides/week_1_intro.tex`,
`slides/week_2_huggingface.tex`, `slides/week_3_effective_llm_use.tex`,
`slides/week_4_classification.tex` and their
matching notebooks. Read `docs/week_2_review.md` for the detailed second-week
choices and `docs/references.md` for source links. Do not link the local attention
animation as an online resource: it has not been published.
