# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Engineering learning project structured as 5 progressive weeks of Jupyter notebooks. The central theme is building a **Digital Twin** — an AI agent that can represent a person — progressively enhanced with more sophisticated capabilities each week.

## Environment Setup

Python virtual environment is at `ai_env/`. Activate it before running anything:

```bash
source ai_env/Scripts/activate   # bash on Windows
```

Required environment variables in `.env` (at repo root):
- `OPENAI_API_KEY` — used in all notebooks
- `PUSHOVER_USER` and `PUSHOVER_TOKEN` — only required for week-3+ tool-calling notebooks

## Running Notebooks

```bash
jupyter notebook
```

Notebooks are in `AI Engineering Part 1/week-N/`. Open and run cells interactively. There are no automated tests or build steps.

## Architecture: Week-by-Week Progression

The project builds concepts incrementally — each week extends the prior:

| Week | Key Concept | Notable Notebook |
|------|-------------|-----------------|
| 1 | OpenAI API basics, conversation history, Gradio UI | `gradio.ipynb` |
| 2 | Prompt caching (LiteLLM), dynamic context | `digital-twin-arch1-dynamic-context.ipynb` |
| 3 | Tool/function calling, external APIs (Pushover) | `digital-twin_arch2_basic_tool_call.ipynb` |
| 4 | Multi-tool handling, loop-based tool execution | `digital-twin.ipynb` |
| 5 | RAG with ChromaDB, embeddings, vector search | `RAG.ipynb` |

## Digital Twin Pattern

The core architectural pattern runs through weeks 2–5:
1. A system prompt defines the AI persona
2. Conversation history is accumulated in a list of `{"role": ..., "content": ...}` dicts
3. Tool calls are handled in a `while` loop checking `finish_reason == "tool_calls"`
4. Each architecture iteration adds new capability (caching → tools → RAG retrieval)

## RAG Architecture (Week 5)

`RAG.ipynb` implements the full pipeline:
1. Text is split into overlapping chunks
2. Chunks are embedded via OpenAI's embedding model
3. Embeddings are stored in ChromaDB (persisted to `week-5/chroma_db/`)
4. At query time, the most similar chunks are retrieved and injected into context

ChromaDB data persists between notebook sessions in `AI Engineering Part 1/week-5/chroma_db/`.

## Key Libraries

- `openai` — chat completions and embeddings
- `litellm` — LLM abstraction with prompt caching support (week 2)
- `gradio` — chat UI (week 1)
- `chromadb` — vector store for RAG (week 5)
- `plotly` — 3D embedding visualizations (week 5)
