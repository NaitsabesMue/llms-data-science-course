# Week 2 — revision notes

11 October 2026. The notebook follows the lecture revised together. Week 1 is unchanged.

The teaching route is: choose a trained model, inspect one prediction, change the task, then measure results on labelled reviews. DistilBERT sentiment, BERT's missing-token example, GPT-2 generation, batching and the original BERT-versus-DistilBERT lab comparison remain.

## Terminology and notation

Use established scientific terminology and conventional notation. Explain unfamiliar terms and symbols where they first appear. For example, `b_c` is the bias, not a “learned offset.” Identify illustrative numbers as illustrations. Distinguish model probabilities from measured correctness.

## Final lecture structure

| Slides | Purpose |
|---|---|
| 1–6 | Introduce the task, distinguish the Transformer architecture from the Python library, explore the Hub, and explain the files to load. |
| 7–9 | Load tokenizer and model from one version; explain weight files and repository code; prepare Python. |
| 10–14 | Follow one review through the pipeline, then inspect token IDs, logits, softmax and label selection. |
| 15–18 | Fill a missing token with BERT; continue “A red toy robot” with GPT-2; explain sampling and conversation roles. |
| 19–20 | Explain devices, including AMD/ROCm support, then batches, padding and the padding mask. |
| 21–23 | Brief the lab; introduce fine-tuning as an outlook through the Coinbase example; provide reading links. |

The standalone model-comparison and download/cache slides were removed. The four optional appendix slides were removed. The main conversation slide no longer introduces chat-template code. Model comparison remains part of the lab, as specified on its briefing slide.

The fine-tuning outlook, added 12 October 2026, shows the first two paragraphs of the supplied Brian Armstrong tweet at a readable size. The complete screenshot remains in `slides/figures/`. Fine-tuning is defined as further training that updates model parameters, distinguished from supplying context in a prompt. The slide links [Coinbase's technical account](https://www.coinbase.com/blog/part-three-owning-intelligence-series), attributes its results to the company and calls for evaluation on examples not used for training. It introduces no additional lab task.

## Notebook changes

The notebook has seven sections, with short code cells separated by explanations and questions. It contains 29 code cells; the original tasks are preserved.

- Setup uses the Week 1 environment and public downloads. Hosted credentials, cache configuration, migration details and precision benchmarking no longer interrupt the lab.
- Tokenizer, configuration and weights are introduced before loading. The loading argument `revision` selects the recorded version ID. The pipeline reuses the loaded classifier instead of loading a second copy.
- One review is traced through text → token IDs → logits → softmax → label. Standard formulas define the logits and softmax; all their symbols are explained.
- `**inputs`, `eval()`, `inference_mode()`, `[0]`, `dim=-1`, `argmax()` and `item()` are explained beside their use. Evaluation mode is already the loading default; it changes dropout behavior, while inference mode disables gradient tracking.
- BERT's missing-token example explains its 30,522-token vocabulary and the five displayed suggestions. The Marseille example remains an exercise.
- Generation uses “A red toy robot” throughout. The notebook defines the three initial generation settings, shows returned text with and without the prompt, then explains sampling settings. Direct `generate()` reuses the pipeline's model and makes removal of prompt token IDs explicit.
- CPU is the default. NVIDIA/CUDA, supported AMD/ROCm and compatible Mac/MPS settings are distinguished. The ROCm build also uses the `cuda` device string.
- Padding is illustrated with the original four movie-review examples before benchmarking. The padding mask is distinguished from learned attention weights.
- The IMDB sample contains 50 reviews from each class, with recorded test row IDs and a fixed seed. All batch sizes and both classifiers use those same rows and the same input limit.
- Provided measurement functions repeat the inspected prediction steps. Accuracy and reviews per second are defined mathematically. Warm-up is excluded, accelerator work is synchronized, and CPU process RSS is distinguished from CUDA/ROCm tensor allocation. MPS GPU memory is not measured.
- The original TextAttack BERT SST-2 checkpoint remains the comparison model. Its generic label names are explained using the documented SST-2 task order; model output IDs are explicitly mapped to IMDB IDs. Generic labels in other checkpoints are rejected unless a mapping is supplied.
- The comparison is a worked experiment followed by questions and error inspection. Unfinished `NotImplementedError` functions were replaced with executable examples; students change inputs and measurements and justify their choice.
- Optional extra models, sentence embeddings, summarization, chat-template execution, precision experiments, hosted calls and the separate cache section were removed from this notebook.
- Private results can be saved under the ignored `local/student/2026-2027/week_2/` directory. The saved record contains model/dataset versions, library versions, selected rows, settings and measurements. No submission requirement was added.

Changing the manual review recomputes the matching pipeline result. Dataset sampling can be rerun without adding a duplicate column. The generation cell can reload GPT-2 even after the preceding BERT reference has been deleted.

## Sources

- [Behind the pipeline](https://huggingface.co/learn/llm-course/chapter2/2) and [pipeline reference](https://huggingface.co/docs/transformers/en/main_classes/pipelines): input preparation, model scores, output interpretation, generation returns and batching.
- [Model loading](https://huggingface.co/docs/transformers/en/main_classes/model): versions and default evaluation mode.
- [BERT documentation](https://huggingface.co/docs/transformers/model_doc/bert) and [GPT-2 model card](https://huggingface.co/openai-community/gpt2): vocabulary outputs and next-token training.
- [PyTorch evaluation mode](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval), [inference mode](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html), [ROCm interface](https://docs.pytorch.org/docs/stable/notes/hip.html) and [AMD compatibility](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html): calculation modes and device support.
- [IMDB](https://huggingface.co/datasets/stanfordnlp/imdb), [SST-2](https://huggingface.co/datasets/stanfordnlp/sst2), [TextAttack model configuration](https://huggingface.co/textattack/bert-base-uncased-SST-2/blob/6746dde1c9f5e0a76e4c3428ffa499ea2ecb49bc/config.json) and [TextAttack model registry](https://textattack.readthedocs.io/en/latest/_modules/textattack/model_args.html): evaluation data and the retained comparison task.

## Validation and remaining checks

The notebook validates against the notebook schema. All 29 code cells parse, cell IDs are unique, and saved outputs and execution counts are cleared.

Offline checks of the measurement functions cover reversed class IDs, generic-label rejection, explicit mappings, partial batches, warm-up exclusion, throughput, separate memory measurements and CPU/CUDA/MPS synchronization. An additional smoke check executes all 29 code cells with test doubles, including changed-review reruns, generation reloads, repeatable balanced sampling, the two-model comparison and JSON export to a temporary local directory. These checks verify code flow, not trained-model predictions or hardware performance.

The available environment has no PyTorch, Transformers, Datasets or plotting packages. No trained-model downloads, actual notebook model execution or accelerator benchmarks were run. A classroom-environment run remains necessary to verify real outputs, download availability and runtimes.
