# State rules

Read STATE.md before acting. Resume its current run only if it matches this task.
For a new task, initialize STATE.md from ../template/STATE.template.md, recording
a distinct run ID, scope, project/output path and start time. Do not reuse old
completion marks as evidence for a new video.

Use pending, in_progress, completed, blocked or skipped. Update the relevant row
when beginning or completing a step and whenever a blocker or scope change occurs.
Record concrete paths, commands and inspection findings; do not record secrets.
A zero script exit code or successful Python compilation is not evidence of a
correct video. Mark rendering blocked when runtime dependencies are absent.
For a read-only/shared skill installation, keep the run's state copy in the output
project and record its path in the handoff rather than overwriting shared state.
