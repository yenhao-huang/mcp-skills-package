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

## 1. Resolve Home And The Approved Inventory

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

1. Read the selected home account's existing SSH public key and its fingerprint
   locally. If it has no suitable key pair, create a dedicated pair on home,
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
