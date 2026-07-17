# Managed Skill Registry

This file is the source of truth for skill libraries searched by `find-skills`.
Search every enabled source in ascending priority order before using fallback
discovery. A registry entry makes a source discoverable; it does not make every
skill in that source trusted or suitable.

## Registry

| Priority | ID | Enabled | Repository | Default branch | Machine catalog | Human catalog | Skill root |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 | `agentic-awesome-skills` | yes | `https://github.com/sickn33/agentic-awesome-skills` | `main` | `skills_index.json` | `CATALOG.md` and hosted workbench | `skills/` |

## Source: `agentic-awesome-skills`

### Discovery contract

- Canonical repository:
  `https://github.com/sickn33/agentic-awesome-skills`
- Stable manifest:
  `https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/skills_index.json`
- Manifest schema:
  `schemas/skills-index.v1.schema.json`
- Human catalog:
  `https://github.com/sickn33/agentic-awesome-skills/blob/main/CATALOG.md`
- Hosted search/workbench:
  `https://sickn33.github.io/agentic-awesome-skills/`
- Skill entry point: the manifest's `path` plus `/SKILL.md`; require the
  resolved path to remain under `skills/`.

The manifest is a JSON array. Its stable required fields are `id`, `path`,
`category`, `name`, `description`, `risk`, `source`, and `date_added`. Optional
metadata can include upstream repository/license fields and plugin target,
setup, or blocking reasons.

### Search procedure

1. Convert the request into several narrow keywords. Include the task,
   platform, artifact, and common synonyms; search one focused term at a time.
2. Retrieve the manifest and search `id`, `name`, `description`, and `category`
   case-insensitively. For example:

   ```bash
   query='frontend design'
   curl -fsSL \
     https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/skills_index.json \
     | jq --arg query "$query" '
         ($query | ascii_downcase) as $q
         | .[]
         | select(
             ([.id, .name, .description, .category]
               | map(. // "") | join(" ") | ascii_downcase)
             | contains($q)
           )
       '
   ```

3. If the phrase returns nothing, repeat with individual terms and synonyms,
   then use the human catalog or hosted workbench for category exploration.
4. Resolve a short candidate list from the manifest. Fetch only each
   candidate's `SKILL.md` and directly referenced files; never load the entire
   library into context.
5. Apply `references/rules/candidate-review.md` before ranking or recommending.

The example command depends on network access, `curl`, and `jq`. Equivalent
web, GitHub API, or local-clone inspection is acceptable when those tools are
unavailable, provided the same canonical manifest and candidate content are
checked.

### Quality, risk, compatibility, and license

- Use `risk`, `source`, `date_added`, optional `plugin.targets`,
  `plugin.setup`, and `plugin.reasons` as leads for manual review.
- `risk: unknown` requires explicit manual inspection and a caveat; it is not a
  safe classification.
- A target marked `blocked` is not recommendable for that host unless the
  recorded blocking reasons are verified as resolved.
- Inspect the candidate instructions and referenced executable files for
  network, credential, data access, dependency, destructive, and unbounded
  execution behavior.
- Trace community or mirrored content to its upstream source. Prefer a
  candidate with clear provenance and recent maintenance when task fit is
  otherwise comparable.
- Check per-skill or upstream license metadata. The aggregator's `LICENSE`
  covers its original code, `LICENSE-CONTENT` covers its original non-code
  content, and third-party exceptions are tracked separately; none of those
  alone proves that a mirrored third-party skill is reusable under MIT.
- Repository popularity is a source-maintenance signal, not proof of an
  individual skill's quality. This catalog does not publish per-skill install
  counts, so do not report them.

### Preview and installation

Determine the current published release from the repository/package metadata,
verify the corresponding tag, and substitute it for `<release>`. Preview one
exact skill ID before installation:

```bash
npx agentic-awesome-skills@<release> --codex --release <release> \
  --skills <exact-skill-id> --dry-run
```

Only after the user approves the reviewed plan, repeat without `--dry-run`.
Use the requested host flag or an explicit safe target path instead of
silently assuming `--codex`. Do not use mutable `main` for a reproducible
install.

### Verification record

- Last verified: `2026-07-17`
- Verified repository HEAD: `8054fad47642039bb8cf821c04bcbcdf253686fb`
- Observed package version: `14.6.0`
- Evidence checked: repository metadata, `README.md`, `skills_index.json`,
  manifest schema, `LICENSE`, `LICENSE-CONTENT`, source attribution document,
  installer options, and candidate path convention.

This record is an audit snapshot, not a permanent version pin. Refresh it when
the source contract, installer, catalog schema, or licensing policy changes.

## Fallback

Use fallback only after all enabled registries have no suitable reviewed match
or a registry is unreachable.

1. Report which registry and search terms were tried, or the exact access
   failure.
2. Search `https://skills.sh/` or run `npx skills find <query>` with the same
   expanded terms.
3. Treat each result as an unregistered candidate and apply the complete
   candidate review. Clearly label its source and fallback status.
4. If no candidate passes review, say that no verified match was found and
   offer to solve the task directly or create a local skill.

Fallback discovery does not silently add a source to this registry.

## Registry Maintenance

To add or change a source, update this file in one change and record:

- a unique ID, priority, enabled state, canonical repository, and default
  branch;
- machine-readable catalog and schema, or a documented deterministic search
  method when no catalog exists;
- human catalog, skill root, entry-point convention, and path-safety boundary;
- available provenance, quality, risk, compatibility, setup, maintenance, and
  license evidence;
- preview/install commands and a pinned/versioned installation strategy;
- fallback behavior, last verification date, immutable revision, and evidence
  inspected.

Before enabling a new source, test that its catalog resolves candidate paths,
inspect at least one candidate end to end, verify license handling, and ensure
an unavailable source does not prevent later registered sources from being
searched.
