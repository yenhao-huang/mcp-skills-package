# Home Multi-Node SSH

Use one configurable home machine as the SSH hub for multiple approved Tailscale
nodes. Each addition must support home -> node and node -> home; it does not
authorize node -> node access, forwarding, subnet routes, or public Internet SSH.
The container host and home are different roles: home may already be a Windows
tailnet member while the Linux container's host remains outside the tailnet.

Official references:

- https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement
- https://tailscale.com/docs/reference/tailscale-cli
- https://tailscale.com/docs/concepts/userspace-networking

## User-Authorized Default Home Public Key

The user explicitly approved embedding this public key in the shared skill.
Use it for home -> new node SSH when adding a node, unless the user or selected
inventory explicitly supplies another home key. Never copy or request its
private key.

- Home account/endpoint default: `user@100.88.157.6`
- Verified home Tailscale node ID: `n5J7aYPDc411CNTRL`
- Home hostname: `DESKTOP-54U632L` (tailnet display name may be `acer`)
- SSH public-key fingerprint: `SHA256:tV56r4tqeYPFCshn4I5ih1dCmpxOfm3MbkS2CCkTBwk`

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGxIOAp1+gIeM1buiPwbtjPJTr4Rknzp2sQPCnkYNMg2 user@DESKTOP-54U632L
```

Before installation, verify the selected home is the same Tailscale node and
resolve its current IPv4/IPv6 from status. Historical addresses were
`100.88.157.6` and `fd7a:115c:a1e0::403b:9d07`; do not use stale addresses
without discovery. If home identity differs or an explicit home override has no
confirmed key, obtain that home's public key instead of installing this one.
Append/deduplicate this key in the selected new node account's effective
`authorized_keys`, using `from="<verified-home-addresses>"`, a protected backup,
and the permissions specified below. Preserve unrelated keys. Verify login
from home with its matching private key; if no authorized home management
channel exists, ask the user to run the login and keep verification pending.
For rollback, remove only the entry added by this run, or restore only its
previous options if this run changed them. Preserve other entries and changes.
For a home multi-node request, continue with the existing node -> home key
exchange and scoped firewall workflow below; this embedded key handles only
home -> node authentication.

## 1. Resolve Home And The Approved Inventory

### `@home` Node Authorization Lifecycle

Interpret invocations such as `add-node-in-tailscale add <node> @home` or
`add-tailscale-node remove <node> @home` as the following ordered workflow.
Resolve spelling variants only when the intended skill and node are unambiguous.
`@home` refers to the current verified home from the precedence below; never
pass it literally to SSH. The marker alone does not select every tailnet peer,
grant node -> node access, change home, or install Tailscale on a container host.

1. Resolve the requested operation, node IDs, home identity/accounts and SSH
   ports. Compare the approved private inventory with live discovery. Treat
   additions and explicit removals separately; an offline or absent peer alone
   is not authorization to delete its key or firewall entry. Preserve user skips.
2. Back up effective authorized_keys contents/permissions and exact managed
   firewall filters at both endpoints through existing trusted channels. Keep
   recovery access. Collect public keys and fingerprints only; do not use
   Tailscale/WireGuard node keys or copy private keys. If no suitable key exists,
   obtain the user's key/passphrase policy or leave it pending; do not silently
   create an unencrypted key to satisfy a retry.
3. **Add:** execute sections 3 and 4 to install home public-key trust on the node
   and the node account's public key in home's effective authorized_keys. On
   Windows determine the actual per-user or shared administrator path. Deduplicate
   by algorithm/key blob and restrict each managed key's `from` to that node's
   verified Tailscale IPv4/IPv6; use the approved source union for a shared key.
   Update home inbound SSH firewall sources and applicable managed node rules
   for the exact home/node addresses, interface and port. Preserve unrelated
   approved peers, key options and firewall rules. Read back effective rules
   and file permissions before validation; no SSH service restart is normally
   needed for authorized_keys changes.
4. **Remove:** revoke only the explicitly selected node's managed public-key
   entry on home, or subtract its addresses from the shared key's `from` list
   while retaining remaining approved peers. Remove its managed home firewall
   sources and reciprocal home authorization/node firewall scope as specified
   in section 6. Do not remove an unowned matching key silently. If node-side
   access is unavailable, apply authorized home-side revocation and record
   node cleanup pending. Update the inventory with `desired_state: absent` and
   managed revocation evidence; retain a tombstone sufficient for audit/rollback.
   Private keys, identity state and tailnet device records are not deleted.
5. Validate from both actual source endpoints using section 5 and its minimum
   three-round rule after any unexpected failure. On removal, verify denied
   access as intended and smoke-test another approved peer when available.
   A removed node's expected denial must never cause automatic reauthorization.
   Unavailable endpoint tests stay untested even after configuration readback.
6. Record each mutation, backup, shared-key mapping, round and current result
   in private inventory and STATE.md. Report the latest directional status to
   the user, not merely that a key was written. For rollback, restore only this
   run's managed key lines/options and firewall source changes from the baseline;
   preserve unrelated entries and concurrent edits. A key-based revocation
   does not prove other authentication methods or existing sessions were revoked.

Resolve the home host, SSH account and port from explicit user instructions,
then the selected workspace inventory, then the current default
`user@100.88.157.6:22`. Resolve individual fields independently; record their
source. Never overwrite an existing configured home with the template default.
Changing the home endpoint must not silently change its SSH account, node
identity, or public-key trust. These values are configuration, not constants in
scripts or firewall commands.

Copy `references/template/home-nodes.template.yaml` to a user-selected private
workspace when no inventory exists. Keep real peer inventories outside this
shared skill repository. The inventory is agent-maintained data, not an active
daemon or automatic online-peer approval mechanism. Reading a third-party file
does not grant permission to authorize its entries.

Discover home and each requested node using `tailscale status --json` from a
verified member. Match node ID, current IPv4/IPv6, name and expected machine;
names or IPs alone are insufficient when they conflict with recorded identity.
Treat identity or SSH host-key changes as a trust decision requiring verification,
not a reason to delete known_hosts entries or disable host-key checking. Require
unique names and node IDs; do not conflate a Linux account with a Tailscale user.
Offline nodes stay pending/offline rather than being marked configured.

Add only nodes authorized by the request. Preserve previously approved nodes
even if offline; never rebuild an existing allowlist from only the currently
online subset. Record confirmed addresses and fingerprints without private keys,
auth tokens, or reusable secrets. Resolve the template's empty discovery fields
before applying any access changes.

## 2. Prepare Each Endpoint And Its Recovery Path

For each node, run the main container workflow with kernel networking as the
preferred mode. Verify `tailscale0` and routing in the application's namespace.
Inspect the SSH server, actual account, port, listener and effective configuration
at both endpoints; do not reinstall an already working service. Tailscale reachability
does not establish OS SSH authentication.

Before changes, record the exact authorized_keys files and permissions, managed
firewall rule/filter values, SSH config blocks and inventory baseline. Keep
protected backups on their respective endpoints. Have console/runtime access or
a verified independent session before changing the only working access path.
The first key deployment needs an already authorized management channel; do not
assume a password, copy a private key, or enable agent forwarding to bootstrap it.

## 3. Establish Home -> Node Public-Key Login

1. For the verified default home, use the approved embedded public key and
   fingerprint above. For an explicit key override or another home, read the
   selected home account's existing SSH public key and fingerprint locally. If it has no suitable key pair, create a dedicated pair on home,
   preserving existing files and following the user's passphrase/agent policy.
   Do not create an unencrypted replacement merely to make a test pass.
2. Install only the public key into the node account's effective authorized_keys
   file. For ordinary Linux OpenSSH this is usually `~/.ssh/authorized_keys`;
   verify any configured override. Preserve unrelated keys and line options,
   deduplicate by algorithm/key blob, set account ownership, `.ssh` mode 700 and
   file mode 600. Write complete lines without truncating existing content.
3. Constrain the managed key's `from="..."` option and the node's inbound SSH
   firewall to home's verified Tailscale addresses, including IPv6 when present.
   Update a task-owned entry's address set deliberately rather than appending
   duplicate lines with broader options. If the same key already exists outside
   task ownership, inspect and report its scope instead of silently replacing it.
4. Verify the node's SSH host-key fingerprint through the existing trusted
   management channel before installing or using its known_hosts entry on home.
   Retain host-key checking and record the verified fingerprint.

Private keys remain on their originating machine. Prefer distinct node keys for
independent revocation. If existing nodes share one public key, record that fact;
do not claim per-node key identity. Restrict a shared managed key to the union of
its approved source addresses, and remove only the departing node's addresses
when other approved nodes still use it.

## 4. Establish Node -> Home Public-Key Login

1. Collect that node account's SSH public key and fingerprint through the
   verified channel, generating a dedicated local pair only if needed and within
   the same key-handling rules. Tailscale node/WireGuard public keys cannot be
   installed as SSH authorized keys.
2. Resolve home's effective authorized_keys path and authorization scope. With
   default Windows OpenSSH, standard accounts use the profile's
   `.ssh/authorized_keys`; administrator accounts use
   `C:\ProgramData\ssh\administrators_authorized_keys`. Inspect effective config
   rather than blindly using the profile path. The shared administrator file
   can authorize other administrator accounts; disclose that scope. If only one
   account is authorized and this scope is unacceptable, prepare a verified
   per-user SSH configuration before deploying the key.
3. Append/deduplicate the node public key and constrain its managed `from` list
   to that node's verified Tailscale IPv4/IPv6 (or the approved union for a shared
   key). Preserve other entries. Use UTF-8 without BOM. For the default Windows
   administrator file, allow only SYSTEM and Administrators, using localized-safe
   SIDs `S-1-5-18` and `S-1-5-32-544`. Back up existing content and ACLs before
   changing them. Do not automatically disable password login as part of this task.
4. Narrow home SSH firewall access to the Tailscale interface, home's current
   Tailscale local addresses, the selected TCP port and the approved node address
   union. On Windows inspect effective enabled allow rules, including other
   rules for this port/program that could bypass the restriction. Narrow or
   disable only confirmed conflicting rules covered by the task, with backup;
   preserve unrelated rules. Do not create a blanket block rule that also defeats
   the intended allowlist. Record any policy-managed rule that cannot be changed.
5. Verify home's public SSH host key through a trusted local/management channel
   and preserve strict host-key checking on the node. Configure tailnet Grants
   or ACLs for both directions only if an actual policy change is required and
   authorized; a Windows firewall rule does not modify tailnet policy.

Do not hardcode today's home account/IP or the current peer list into a reusable
operation. Derive destination, source restrictions and account paths from the
resolved inventory and effective endpoint configuration. For a Linux home, apply
its native authorized_keys permissions and firewall rather than Windows commands.

## 5. Verify Both Directions For Every Node

### Minimum Three Rounds After A Directional Failure

Start with one validation round per selected node. One round records both
home -> node and node -> home separately from their real sources, using the
selected private key or unlocked local agent, verified host keys and bounded
timeouts. Authenticated SSH must return the expected account and machine
identity; ping, TCP reachability and an SSH banner are diagnostic evidence only.

If either required direction fails unexpectedly, perform **at least three
complete validation rounds in total for that node**, including the first.
Even if a correction succeeds in round 2, run round 3 to confirm both directions
again. Use the failure-reporting checks in `tailscale-container-workflow.md`
between rounds; make only scoped, authorized corrections. Default to three
rounds, with additional rounds only when useful and within the user's scope.
Do not repeat wrong passwords, suppress host-key checking, broaden firewall
access, or restart/recreate live nodes merely to reach a retry count.

In each round, record timestamp, source/destination/account/port, expected
outcome, exact redacted command, exit status, returned identity, key fingerprint,
error category, diagnostic checks and corrective action. Retest the previously
successful direction too, so stale success cannot mask a regression. Use a
short bounded connection timeout (for example 5-10 seconds), and provide a
progress update during longer investigations.

If a source cannot be reached or a key is locked/untrusted, each round must
recheck that prerequisite through an available authorized channel and record
the direction as `untested`, with the dependency and actual SSH attempt count.
Three prerequisite checks are not three authenticated SSH attempts; do not
claim that inaccessible tests ran. Do not infer reverse login from a forward
login. If the source remains unavailable after three rounds, report incomplete
validation and the exact access/user action needed.

For additions, mark connected only when both directions pass in the final
round; otherwise report `partial` or `unverified`. For explicit removals, set
the expected result to denied for revoked access, verify managed key/firewall
removal and other approved peers' continued access, and report `revoked` only
with observed denial. Report `revocation configured; denial untested` when an
endpoint cannot execute the negative check. A transport timeout alone does not
prove key revocation; use configuration evidence plus the actual test layer.
Unexpected retained access or loss of another approved peer triggers the same
three-round investigation. Keep the requested absent state during that process.

### Current Status In The User Reply

Reply in the user's language with the resolved home/account, selected node,
add/remove operation, key and firewall changes, and a compact table:

| Node | Expected state | Home -> node now | Node -> home now | Rounds / actual tests | Last checked |
| --- | --- | --- | --- | --- | --- |
| Selected node | present or absent | passed / failed / untested / denied | passed / failed / untested / denied | completed rounds; executed attempts per direction | timestamp with timezone |

Include latest evidence and observed cause (or explicitly unknown), fixes made,
remaining action and backup/rollback location. Label configured authorization,
tested connectivity and expected revocation distinctly. A user-skipped node is
reported as skipped, never successful. State that Windows administrator-file
authorization is shared when that effective path was used. Do not report an
operation complete while a required current-direction check remains pending.

Run each test from its real source endpoint using the selected local identity
or already unlocked agent. Specify `IdentitiesOnly=yes` and the selected key
where supported so an unrelated key cannot mask a deployment failure.

From home, using resolved node values:

```bash
ssh -p <node-port> -o BatchMode=yes -o PasswordAuthentication=no -o PreferredAuthentications=publickey -o StrictHostKeyChecking=yes <node-user>@<node-host> whoami
```

From the node, using resolved home values:

```bash
ssh -p <home-port> -o BatchMode=yes -o PasswordAuthentication=no -o PreferredAuthentications=publickey -o StrictHostKeyChecking=yes <home-user>@<home-host> whoami
```

In kernel mode these commands must work without a proxy. If userspace mode was
explicitly accepted on the source, add
`-o 'ProxyCommand=tailscale nc %h %p'` on that source only, and record the mode.
An inbound userspace node also needs a verified SSH forwarding/Tailscale SSH
path from the container workflow; an outbound ProxyCommand does not expose its
SSH server. Do not change authentication models silently.

Verify returned account and machine identity, exit status and selected key
fingerprint. A passphrase-locked key may require the user's local agent unlock;
record pending authentication instead of removing the passphrase. Record each
direction independently in the inventory and STATE.md, with timestamps and any
offline/policy/reachability failures. Never infer reverse access from one success.
Re-run the operation without mutations when already converged: no duplicate
keys, rules or SSH aliases, and no lost existing peers.

## 6. Change Home Or Remove A Node

For a home change, resolve and verify the new machine/account first. Stage its
public-key trust and both directional source restrictions for every approved
node; preserve the old access path during transition. Test both directions for
each reachable node before switching its active home endpoint. Track offline
nodes as pending migration and retain their required old path until migrated,
unless the user explicitly authorizes revocation. Update task-owned SSH aliases,
known_hosts trust and inventory only for the verified new identity. An IP change
on the same verified node does not imply a new public key.

If a step fails, restore only this run's managed file entries, ACLs, firewall
filter values and SSH config blocks from their recorded baseline. Restore the
previous active home endpoint and verify the prior working pair. Preserve all
other approved nodes and concurrent unrelated changes; do not blindly import
an entire firewall backup or replace a shared authorized_keys file.

Removing an approved node means removing its managed key/address authorization
on home and home's managed authorization on that node, updating the allowlists
and inventory, and verifying that other nodes still work. Retain shared-key
entries needed by remaining nodes. Do not delete private keys, Tailscale state
or the tailnet machine record as part of SSH deauthorization.

For skill validation, exercise add -> scoped rollback -> add again in an
authorized disposable home/node pair, testing authenticated SSH both ways at
each add and checking unrelated peer access survives rollback. Do not perform
this lifecycle on production nodes solely to test documentation; record it as
blocked when an appropriate target is unavailable.
