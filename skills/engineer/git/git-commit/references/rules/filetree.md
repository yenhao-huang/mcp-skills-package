# Filetree Rules

- Stage only files that belong to the logical change being committed.
- Preserve unrelated tracked, untracked, and user-authored changes.
- Never stage `.env`, credential files, private keys, generated secrets, or
  other sensitive material.
- Inspect staged file names and `git diff --cached` before committing.
- Do not create helper files solely to construct a commit message.
