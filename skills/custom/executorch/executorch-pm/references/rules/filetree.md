# Filetree rules

Skill source: `skills/custom/executorch/executorch-pm/`. Installed copy: `~/.codex/skills/executorch-pm/`.
Keep SKILL.md, STATE.md, references/rules/{filetree,env,state-rules}.md and references/template/STATE.template.md.
Keep domain references under references/. Preserve unrelated project files.

Project exception: executorch-pm/template/ contains issue-disptach.html and Result.md output templates (HTML source for PDF export and Markdown results), as explicitly requested by the user. These templates never go to daily.

Shared dependencies: skills/content-producer/{humanizer,frontend-slides}/.
Install both alongside PM when using flat skill folders; do not recreate private
copies under PM. Keep the PM presentation template and output rules here.

issues.json at the PM skill root is persistent recommendation history. Preserve installed entries on upgrades; never reset or copy this file into daily.
