# Candidate Review Rules

Use this checklist for every candidate before recommending or installing it.

## Task Fit

- Read the full `SKILL.md`, not only catalog metadata.
- Confirm trigger conditions, outputs, workflow, and prerequisites match the
  user's concrete task and target host.
- Check for conflicting assumptions about repository layout, tools, runtime,
  operating system, network access, or user interaction.

## Provenance And Maintenance

- Record the registry, candidate ID/path, aggregator source field, original
  upstream repository when applicable, and a direct candidate link.
- Distinguish official, first-party, mirrored, and community sources.
- Check recent repository activity and unresolved maintenance/security signals
  when available. Do not substitute stars or popularity for content review.

## Risk And Security

- Record the catalog risk label without treating it as authoritative.
- Inspect all directly referenced scripts and executable instructions.
- Identify filesystem writes, deletion or overwrite behavior, shell execution,
  package installation, network calls, secrets, credentials, external messages,
  privilege requirements, and unbounded agent/tool loops.
- Reject path traversal, hidden payload retrieval, unjustified destructive
  behavior, or instructions that bypass approval and safety controls.
- State remaining uncertainty. Recommend a sandbox or manual adaptation when a
  useful skill cannot safely run as published.

## Compatibility And Setup

- Verify the requested host is supported and review all setup requirements and
  blocking reasons.
- Check referenced files exist under the expected skill root or at a documented
  upstream location.
- Treat unresolved local-only references or missing dependencies as blocked,
  not as minor caveats.

## License

- Find an explicit per-skill or upstream license and link its source.
- Do not assume an aggregator's root license covers mirrored third-party work.
- Mark the license `unknown` when no reliable declaration exists and explain
  that reuse or redistribution may require permission.

## Recommendation Gate

A recommendation must include task fit, provenance, host compatibility,
risk/security findings, license, maintenance evidence, exact link, and a pinned
preview/install method when available. Exclude a candidate when a material
issue is unresolved; if it remains useful for comparison, label it as blocked
and do not provide an executable install step as though it were approved.
