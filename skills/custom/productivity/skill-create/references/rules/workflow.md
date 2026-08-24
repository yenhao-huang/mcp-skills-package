# Workflow And Reversibility Rules

Use this reference before creating or changing a skill workflow, installation
steps, rollback behavior, or validation plan.

## Required Workflow

Every new or substantially updated skill must contain a `## Workflow` section
in `SKILL.md`. The section must use ordered, executable steps and identify:

1. the context that must be read before mutation;
2. the action or mutation to perform;
3. the validation that proves the requested outcome; and
4. the evidence to record in `STATE.md` when the skill tracks state.

A list of principles without an execution order does not satisfy this
contract.

## Reversibility Contract

Apply this contract whenever a skill is intended or claimed to be reversible.
For every workflow step that installs, creates, starts, enables, or configures
a component, identify that component as A and provide a matching rollback step
for the same A.

If the workflow teaches `install A`, it must also teach how to uninstall A or
restore the exact pre-install state. Generic advice such as "clean up" or
"undo the change" is insufficient. The rollback instructions must identify
the affected files, packages, services, containers, configuration, or other
state closely enough to execute safely.

Rollback must preserve unrelated user state. If safe rollback cannot be
defined, the skill must not claim reversibility and must state the limitation.

## Validity Check

Validate every reversible installation path in an isolated, disposable, or
otherwise safely recoverable target using this exact lifecycle:

```text
install A -> rollback/uninstall A -> install A again
```

At each transition, verify and record observable evidence:

1. After the first install, prove A is present and functional.
2. After rollback, prove A and only A's managed state were removed or restored.
3. After the second install, prove A is present and functional again without
   relying on state left by the first install.

Record the commands, target environment, assertions, and results in
`STATE.md`. Static review, documentation review, or a successful first install
alone does not pass this validity check. If the lifecycle cannot be run safely,
mark validation `blocked` and do not report the skill as valid or complete.
