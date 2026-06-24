---
name: project-convention
description: Standardize project structure for models, datasets, and environment management
---

## When to use
- Setting up a new ML / LLM project
- Refactoring an existing repository
- Preparing for reproducibility, collaboration, or deployment

---

## File Tree

Use this structure strictly. New files and directories must be placed in the matching location below; do not create alternate top-level directories unless the user explicitly requests it or the existing project already has a conflicting established structure.

.
├── data/              # project-specific data (intermediate / temp)
├── logs/              # runtime logs
├── lib/               # shared utilities
├── test/              # test cases
├── external/          # third-party services (vllm, llama-server, etc.)
├── configs/           # config files (yaml/json/env templates)
├── core/
│   ├── api/           # API layer (FastAPI / routes)
│   └── service/       # business logic / pipelines
├── ui/                # frontend / interface
├── results/           # evaluation outputs
├── exp/               # experiments / research
├── docs/              # project documentation
├── .gitignore
├── AGENT.md           # Codex/agent project instructions
├── CLAUDE.md          # Claude project instructions
└── README.md

---

## Instructions

Follow these rules strictly.

---

### 1. Models (Global)

- Store ALL models in:
  ~/Desktop/models/

- Includes:
  - LLM weights (GGUF / HF / vLLM)
  - embedding models

- Rules:
  - NEVER store models inside the repository
  - ALWAYS reference via environment variables

---

### 2. Datasets (Global)

- Store shared datasets in:
  ~/Desktop/datasets/

- Structure:
  ~/Desktop/datasets/
  ├── humaneval/
  ├── gsm8k/
  ├── mmlu/
  └── <dataset>/

- Rules:
  - Shared across projects
  - NEVER commit datasets into repo
  - ALWAYS use symlink

- Command:
  ln -s ~/Desktop/datasets ./data

---

### 3. Environment Setup

- Create virtual environment:

  python -m venv .venv
  source .venv/bin/activate
  uv pip install -r requirements.txt

- Python version:
  python==3.12

- Create:
  ./.env

- Store:
  - API keys
  - model paths
  - dataset paths
  - DB configs

### 4. Git Ignore

For new projects, create `.gitignore` from `references/.gitignore.template`.
Read that template before scaffolding `.gitignore`, and copy its contents exactly unless the target project convention explicitly overrides it.

---

## Summary

Centralize models and datasets globally, keep repositories lightweight, and ensure reproducibility via environment variables and symbolic links.
