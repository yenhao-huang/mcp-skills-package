# Filetree rules

Skill source: `skills/custom/executorch/executorch-pm/`. Installed copy: `~/.codex/skills/executorch-pm/`.
Keep SKILL.md, STATE.md, references/rules/{filetree,env,state-rules}.md and references/template/STATE.template.md.
Keep domain references under references/. Preserve unrelated project files.

Project exception: executorch-pm/template/ contains issue-disptach.html and Result.md output templates (HTML source for PDF export and Markdown results), as explicitly requested by the user. These templates never go to daily.

Vendored dependency exception: references/frontend-slides/ preserves upstream relative layout, including scripts/ and the style pack, with LICENSE and SOURCE.md. Its nested SKILL.md is reference material loaded by PM, not a separate managed skill.
