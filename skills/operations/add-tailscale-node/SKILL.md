---
name: add-tailscale-node
description: Add or manage a Linux container Tailscale node and connect it bidirectionally to a configurable home machine. Use for add-node-in-tailscale requests, @home public-key and firewall synchronization on node addition/removal, home multi-node SSH, Docker or LXC kernel networking, userspace migration, or safe removal without enrolling the container host.
---

# Add Tailscale Node

Manage Tailscale inside a container without enrolling the container host in the
tailnet.

## Required Context

Read these files before acting:

- `references/rules/env.md`
- `references/rules/filetree.md`
- `references/rules/state-rules.md`
- `references/tailscale-container-workflow.md`

Reset `STATE.md` from `references/template/STATE.template.md` for a new run,
then record concrete evidence as each phase progresses.

For home multi-node setup, read `references/home-multi-node.md` and use
`references/template/home-nodes.template.yaml` as the non-secret inventory.
For home -> new node SSH, use the user-authorized default home public key
embedded in `references/home-multi-node.md`, unless explicitly overridden.
A request to add a new node includes installing this key for the selected node
account after verifying home identity and source addresses. For home multi-node
requests, retain both SSH directions required by the workflow below.
The current home default is `user@100.88.157.6`; it is an overridable connection
setting, never a fixed identity or an instruction to alter that machine.

`@home` selects the resolved current home as the SSH authorization hub. It is
an invocation marker, not a literal hostname or a request to enroll home.
Read the `@home` lifecycle section of `references/home-multi-node.md`: adding
a selected node installs its SSH public key on home and home public-key trust
on the node, synchronizes scoped firewall rules, and verifies SSH both ways.
Explicit removal revokes that node's managed key/source authorization and
firewall access, preserving shared-key peers. It does not delete tailnet identity.

## Workflow

1. Resolve the exact target container and runtime before mutation. If the user
   means the current container, inspect that environment; do not infer its
   boundary from an empty nested `docker ps` or create another container.
2. Adding a node defaults to both directions between the node and the resolved
   home/peer, including authenticated SSH. Honor an explicit narrower user scope.
   Resolve the peer from user input, then inventory, then the documented home
   default; identify the actual accounts, protocols and ports.
   For home multi-node requests, resolve home from explicit user input, then
   the selected inventory, then the default. Adding a node in this mode includes
   both home -> node and node -> home SSH; follow the home reference to exchange
   public keys, update exact peer allowlists and validate each direction.
3. Inspect the container before mutation: distro, init system, installed
   binaries, daemon state, `/dev/net/tun`, Linux capabilities, state path, and
   current Tailscale identity.
4. Prefer kernel networking for a new node and ordinary direct SSH. Follow
   the kernel setup and migration sections in the workflow reference. Verify
   TUN access and `NET_ADMIN`; preserve the existing node state and runtime
   configuration. If kernel mode is requested but unavailable, report the
   required runtime change rather than substituting userspace mode. Use the
   userspace proxy path only when requested or accepted by the user.
5. Verify current commands against official documentation, install only inside
   the target container, authenticate without exposing secrets, and configure
   only the required traffic. Record changed files, supervisor settings, and
   the matching rollback procedure in `STATE.md`.
6. For removal, first determine whether the user wants a disconnect, package
   uninstall with identity preserved, or complete removal. Treat state deletion
   and tailnet device deletion as separate destructive actions.
   With `@home`, apply the explicit add/remove authorization lifecycle even if
   no package changes are needed; record skipped or unreachable node cleanup.
7. Validate both directions with real application clients from each actual source.
   For a default node addition, follow `references/home-multi-node.md` to
   establish and test authenticated SSH both ways. Enrollment, ping, an open
   TCP port or an SSH banner alone never completes the addition. If either
   direction fails, diagnose it using the failure-reporting section of the
   workflow reference and run at least three complete validation rounds for
   that node, testing both directions in each round when source access permits.
   An initial failure followed by recovery still requires all three rounds.
   Record unexecutable tests as untested, not passed or attempted SSH commands.
   Report the final current communication state, evidence and remaining actions;
   additions remain partial until both directions pass in the final round.
   For explicit removal, expected revoked access is a successful revocation
   check, not a failure to repair by restoring authorization.
   For kernel mode, prove that `tailscale0` and policy routing exist in the
   application container and normal SSH works without a proxy. Confirm the
   host itself was not enrolled or exposed, and record evidence and limitations
   in `STATE.md`.

## Guardrails

- Do not install or authenticate Tailscale on the host unless explicitly asked.
- Do not use host networking for a container-only integration.
- Missing Docker device mappings or capabilities require a runtime change and
  usually container recreation. Prepare the exact change while preserving
  mounts, identity state, application configuration, and a recovery path; do not
  restart or recreate a live node merely to edit this skill.
- When changing the only remote access path, establish console/runtime access
  or another verified recovery channel before stopping `tailscaled`.
- Never print, persist in shell history, or commit an auth key. Prefer a secret
  file, orchestrator secret, or interactive login URL.
- Do not publish host ports unless the user explicitly requests host access.
- Never delete `/var/lib/tailscale/tailscaled.state`, a state volume, or the
  tailnet machine record without explicit confirmation of complete removal.
- Do not stop unrelated processes. Resolve the exact `tailscaled` PID or service
  unit before stopping it.
- Tailnet membership or online status alone does not approve a peer for home SSH.
  Preserve existing approved peers, restrict additions to the requested nodes,
  and never transfer private keys or treat Tailscale node keys as SSH keys.

## Output

Always report a per-direction result (passed, failed, or untested), the actual
source/destination and account, and evidence. For each failure or untested
direction, explain the observed cause or explicitly state that it is unknown,
the checks performed, and the next concrete action or missing access needed.
Do not describe untested authenticated SSH as successful connectivity.

Report the selected networking mode, commands or changes made, connectivity
validation, host-isolation result, uninstall level if applicable, and any
restart or persistence limitation.
For home multi-node runs, also report the resolved home endpoint and a per-node
matrix of both SSH directions, public-key fingerprints, pending/offline nodes,
and the inventory and rollback paths. For `@home`, include operation (add/remove),
key/firewall changes, actual/required validation rounds, last check timestamp,
and current home -> node / node -> home results in the user's language. Do not
substitute historical success for the current round or claim expected denial
was observed if only configuration readback was possible.
