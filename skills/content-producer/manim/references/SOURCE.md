# Source and adaptation

- Upstream: [AmitSubhash/3brown1blue](https://github.com/AmitSubhash/3brown1blue).
- Pinned commit: [fd9bf9c69ac33519acc00dc7faa21bd14b241e54](https://github.com/AmitSubhash/3brown1blue/commit/fd9bf9c69ac33519acc00dc7faa21bd14b241e54).
- Source directory: [src/three_b1b/skill](https://github.com/AmitSubhash/3brown1blue/tree/fd9bf9c69ac33519acc00dc7faa21bd14b241e54/src/three_b1b/skill).
- License: [MIT text and copyright notice](LICENSE), preserved from upstream.

All files in the upstream skill directory are included. The original SKILL.md
is adapted as guide.md; technical rules, audience/domain profiles and helpers
live under references/. Upstream templates/ becomes references/template/.
The design-visual README becomes designing-math.md; its demo joins the templates,
and the three PNGs remain under assets/designing-math/.

Local changes add the package entry workflow, environment/layout/state rules,
blank run state/template and profile index. Local resource links and template
path examples are rewritten, the demo imports adjacent style.py, and Claude-only
wording is generalized. The helper scripts retain their upstream behavior.
The entry point documents overwrite/path limitations and distinguishes helper
execution from actual visual review.

The upstream Python CLI, agent launcher, model services, speech providers and
package installer are not included. Optional upstream CLI examples need those
components separately. No rendered-output compatibility claim is made by this
packaging change; runtime validation must use the target project's environment.
