---
name: codex-review
description: Enforce development workflow, commit structure, and safety constraints for Codex-generated changes
---

## When to use
- Any code modification in this repository
- Before creating commits
- Before performing remote upload
- When validating compliance of changes

---

## Instructions

Follow ALL rules strictly. Do not proceed if any rule is violated.

---

## 1. Workflow Control

- ALWAYS work on branch: `codex`
- NEVER commit or push directly to `main`
- If current branch is not `codex`, STOP and request switch
- DO NOT create new branches unless explicitly instructed

---

## 2. Version Control Policy

Every commit MUST:

- Start with prefix: `[codex]`
- Have a concise summary (<= 72 characters preferred)
- Include a blank line after title
- Include EXACT sections:

Design:
Testing:

---

### Commit Template

[codex] short summary of change

Design:
- Goal:
- Approach:
- Alternatives considered:
- Complexity/Performance:
- Concurrency/Safety:
- Limitations:
- Scope:

Testing:
- Build status:
- Unit tests:
- Manual verification:
- Edge cases checked:
- Known risks:

---

## 3. Change Scope Control

- Modify ONLY files directly related to the task
- DO NOT refactor unrelated modules
- DO NOT rename/reformat unrelated code
- Keep diff minimal and scoped
- Avoid multi-purpose commits

---

## 4. Design Requirements

Each commit MUST include:

- Goal: problem being solved
- Approach: high-level method
- Alternatives considered: at least ONE
- Complexity/Performance: if relevant
- Concurrency/Safety: must be addressed (even if N/A)
- Limitations: at least ONE
- Scope: explicitly state what is NOT changed

Design must explain reasoning, not just code changes.

---

## 5. Testing Requirements

Each commit MUST include:

- Build status: success / not run (+ reason)
- Unit tests: executed / not applicable
- Manual verification: what was tested
- Edge cases checked: if any
- Known risks: if any

Testing section MUST NOT be empty.

---

## 6. Large Change Protocol

If change affects:

- Concurrency model
- Network protocol
- Database schema
- Core service logic
- Public API behavior

THEN:

- DO NOT modify code immediately
- FIRST produce a standalone design proposal
- WAIT for approval before proceeding

---

## 7. Safety Constraints

- DO NOT introduce blocking calls in async/event-driven code
- DO NOT introduce global mutable state without approval
- DO NOT silently change public API behavior
- DO NOT remove error handling unless instructed
- PRESERVE backward compatibility unless instructed otherwise

---

## 8. Pre-commit Self-check

Before committing, VERIFY:

- Design includes ≥1 alternative
- Design includes ≥1 limitation
- Concurrency/Safety is addressed
- Testing section is complete
- Diff is minimal and scoped
- No unrelated files modified

IF ANY check fails → DO NOT COMMIT

---

## 9. Remote Upload Protocol (GitHub MCP ONLY)

- NEVER use `git push` for remote updates

When user says:
- "上传远端"
- "Upload remote"

MUST:

1. Summarize:
   - changed files
   - intent

2. Confirm:
   - target branch (default: `codex`)

3. Ensure:
   - commit message follows rules

4. Perform upload via GitHub MCP API ONLY

5. After upload, output:
   - branch name
   - commit SHA (or equivalent)
   - list of updated files