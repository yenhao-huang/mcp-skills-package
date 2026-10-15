# File layout

`SKILL.md` is the entry point. `STATE.md` records this skill's validation run;
use the template for subsequent local operating runs. Required reusable rules:
`references/rules/{env,filetree,state-rules}.md`; state template:
`references/template/STATE.template.md`.

Domain references are `references/topology.md`, `deployment.md`, `lifecycle.md`.
Executable helpers/tests belong to `references/scripts/`. Do not commit generated
Compose containing credentials, Docker inspections, tokens, model weights, raw
corpus, runtime logs or __pycache__. Host deployment/evidence paths are documented
in topology; they are not repository assets.
