# Pull Request Body Template

Use a repository-provided PR template first. Use this fallback only when no
suitable template exists.

```markdown
## Summary

- Describe the user-visible or operational outcome.
- Describe the main implementation choice.

## Changes

- List the important code or configuration changes.

## Validation

- `command`: result

## Risks

- Describe known risks, compatibility concerns, migrations, or rollback needs.
- Write `None identified` only after reviewing the full PR diff.

## Related Issues

Refs #123
```

Replace `Refs` with `Closes` only when merge should automatically close the
issue.
