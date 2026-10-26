# Filetree rules

Skill source: `skills/custom/executorch/executorch-pm/`. Installed copy: `~/.codex/skills/executorch-pm/`.
Keep SKILL.md, STATE.md, references/rules/{filetree,env,state-rules}.md and references/template/STATE.template.md.
Keep domain references under references/. Preserve unrelated project files.

Project exception: executorch-pm/template/ contains issue-disptach.html and Result.md output templates (HTML source for PDF export and Markdown results), as explicitly requested by the user. These templates never go to daily.

Shared dependencies: skills/content-producer/{humanizer,frontend-slides}/.
Install both alongside PM when using flat skill folders; do not recreate private
copies under PM. Keep the PM presentation template and output rules here.

issues.json at the PM skill root is persistent selection/handling/exclusion state. Preserve installed entries on upgrades; never reset or copy this file into daily.

recommendation-history.json at the PM skill root records published candidate IDs separately from issue selection/handling status. Preserve installed history on upgrades; backfill verified historical batches when empty. Never copy the ledger into daily.

ci-investigations.json at the PM skill root is the persistent reviewed-CI-failure cache. Preserve installed records on upgrades; initialize only when absent. Never publish it to daily. Detailed read-only triage rules live in references/ci-triage.md.
