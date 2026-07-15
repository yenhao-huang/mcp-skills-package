# Environment Rules

Primary language: Markdown instructions
Runtime version: Git 2.x
Package manager: None
Frameworks: None
Service manager: None
Required services: A local Git repository

- Run Git commands from the target repository root unless the repository
  explicitly documents another working directory.
- Do not install packages or modify global or repository Git configuration.
- Do not read credential stores, private keys, or unrelated files outside the
  repository.
