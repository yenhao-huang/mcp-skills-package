# Environment

Primary language: Python 3.12. Package manager: uv. Frameworks: DeerFlow harness, LangChain/LangGraph, PyMuPDF. No Docker/Gateway/UI services are required.

Use a dedicated .venv under an explicitly selected runtime. Resolve it with --framework-root, DEER_RESEARCH_ROOT or the caller's .deer-flow-research-runtime. No user-specific absolute path is assumed. Install/rollback instructions are in references/runtime.md.

Default authentication is the existing Codex login via the upstream loader; never copy or print credentials. API mode is optional and explicit. Local extraction/protocol tests make no provider calls.

Inputs remain in their original locations. Outputs default to the caller's results/start-deer/<timestamp>/, separately from dependencies. Existing job directories are rejected. Original files and prior corpora are not overwritten.
