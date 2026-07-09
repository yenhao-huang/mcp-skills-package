# Repo Create Filetree Rules

Use this reference before adding, moving, or removing files while using the
repo-create skill.

## Skill Directory Layout

This skill must keep the repo-local skill layout:

```text
repo-create/
|-- SKILL.md
|-- STATE.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- example.md
|   |-- governance-docs.md
|   |-- rules/
|   |   |-- env.md
|   |   |-- filetree.md
|   |   `-- state-rules.md
|   `-- template/
|       `-- STATE.template.md
```

## Target Repository Docs

When this skill creates governance docs in a target repository, prefer:

```text
AGENTS.md
docs/
|-- feature-list.md
`-- rules/
    |-- environment.md
    `-- filetree.md
```

Do not create additional top-level directories unless the user agrees or the
target repository already uses them.
