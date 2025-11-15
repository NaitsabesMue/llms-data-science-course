# Large Language Models in Data Science (WIP)

This repository contains materials for a **21-hour lecture** titled:

> **Large Language Models in Data Science**  
> *Embeddings, Prompting, Retrieval & Applied Use Cases*

---

## 🎯 Course Objectives

- Understand how modern LLMs work: tokens, embeddings, transformer architecture, and inference.
- Use pretrained models via Hugging Face and API-based LLMs in a reproducible way.
- Design effective prompts and retrieval-augmented generation (RAG) pipelines that use embeddings and keyword search.
- Compare different approaches (regex rules, classical ML, HF models, zero-shot LLMs, RAG) in terms of quality and latency.
- Evaluate model performance with simple but meaningful metrics (accuracy, latency, precision/recall, grounding) and apply LLMs to real data science tasks (analysis, reporting, feature generation, code assistance).

---

## 📚 Structure

- **Language**: English  
- **Audience**: Final-year data science students with strong math background  
- **Total Time**: 21h  
  - Lectures: ~7h  
  - Labs: ~7h  
  - Hackathon: ~7h (final evaluation)

---

## 💻 Content

| Folder | Description |
|--------|-------------|
| `slides/` | LaTeX slide decks for all lectures |
| `labs/` | Jupyter notebooks for hands-on experimentation |
| `examples/` | Prebuilt pipelines: OpenAI API, RAG demos, etc. |
| `projects/` | Hackathon templates and ideas |
| `data/` | Data sets |

---

## 🧪 Final Evaluation: Hackathon

The final mark (out of 20) will be based on participation in a **group hackathon** (teams of 1 to 5 participants). Each team will present a project that uses LLMs in a data science context.

### 🔍 Evaluation Breakdown (4 x 5 points)

| Criterion | Description |
|----------|-------------|
| **1. Use Case & Applications (5 pts)** | Relevance, originality, and potential future usefulness of the proposed use case |
| **2. Code Cleanliness (5 pts)** | Code readability, organization, comments, modularity, and reproducibility |
| **3. Lecture Integration (5 pts)** | Use of concepts covered in the course: prompting, fine-tuning, RAG, etc. |
| **4. Presentation (5 pts)** | Clarity, conciseness, visuals, and ability to explain design decisions |

> 💡 Your final score out of 20 is your **official course grade**.

---

## 📅 Timeline

Materials for Weeks 1–6 (lectures, labs, and hackathon template) are available in this repository. Future iterations may refine content and add additional examples.

---

## 🗓️ Weekly Materials

### Week 1 – LLMs: A Primer
- Slides: `slides/week_1_intro.tex`
- Lab: `labs/week_1_tokenization.ipynb`
- Readings: [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/), [OpenAI GPT Models Documentation](https://platform.openai.com/docs/guides/gpt), [Attention Is All You Need](https://arxiv.org/abs/1706.03762)

### Week 2 – Hugging Face & Transformers: Using Pretrained Models
- Slides: `slides/week_2_huggingface.tex`
- Lab: `labs/week_2_huggingface_basics.ipynb`
- Docs: [Transformers Overview](https://huggingface.co/docs/transformers/en/index), [Datasets](https://huggingface.co/docs/datasets), [Hugging Face Hub](https://huggingface.co/docs/hub)

### Week 3 – Effective LLM Use: Coding, Research, Ideation, First Analysis
- Slides: `slides/week_3_effective_llm_use.tex`
- Lab: `labs/week_3_effective_llm_use.ipynb`
- Notes: The lab uses the Gemini API. Set an environment variable `GEMINI_API_KEY` (e.g., add it to `.env`) and install `google-generativeai` before running.

### Week 4 – Text Classification and Intent Routing
- Slides: `slides/week_4_classification.tex`
- Lab: `labs/week_4_classification.ipynb`
- Notes: Build and compare several intent classifiers (regex rules, embeddings + logistic regression, zero-shot NLI, LLM prompting) for an AMU student chatbot; analyse accuracy and latency trade-offs.

### Week 5 – Retrieval-Augmented Generation (RAG)
- Slides: `slides/week_5_rag.tex`
- Lab: `labs/week_5_rag.ipynb`
- Notes: Construct a small RAG system over an AMU / Data Science corpus; explore BM25 vs. embeddings vs. hybrid retrieval; observe how augmented prompts change answers and reduce hallucinations.

### Week 6 – Hackathon: Applied LLM Projects
- Slides: `slides/week_6_hackathon.tex`
- Template: `labs/week_6_hackathon_template.ipynb`
- Notes: One-day team hackathon (1–5 students) to design and implement a small end-to-end LLM/RAG project in a GitHub repository, then present a short demo. See the “Final Evaluation: Hackathon” section above for grading criteria.

---

## 📬 Contact

Instructor: _Sebastian Mueller_  
University: _Aix-Marseille Université_  
Course code: _TBD_
