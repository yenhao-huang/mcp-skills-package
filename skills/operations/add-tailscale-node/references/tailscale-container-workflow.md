# Add Tailscale Node Workflow

Use this reference for installation, existing-container integration,
connectivity validation, and removal. Re-check current syntax against official
Tailscale documentation before executing commands because package and CLI
behavior can change.

Official references:

- https://tailscale.com/docs/install/linux
- https://tailscale.com/docs/concepts/userspace-networking
- https://tailscale.com/docs/reference/tailscale-cli/serve
- https://tailscale.com/docs/features/client/uninstall?tab=linux
- https://tailscale.com/docs/features/containers/docker
- https://tailscale.com/docs/features/containers/docker/docker-params

## 1. Define The Boundary

Establish all of the following before changing anything:

- Whether the target is this execution container, an existing container managed
  by the accessible runtime, or a new container explicitly requested by the user.
  Inspect `/.dockerenv`, `/proc/1/cgroup`, namespaces and runtime metadata as
  available. An empty nested `docker ps` does not identify the current shell's
  boundary or authorize creating a nested container.
- Container runtime and exact container or pod name.
- Whether commands run inside the container or through the runtime from the
  host.
- Connection direction: cluster to container, container to cluster, or both.
- Required protocol and port for every service.
- Whether the container may be recreated.
- Whether Tailscale state must survive a container restart or replacement.

Container-only means:

- The host is not installed, authenticated, or registered as a Tailscale node.
- The container does not use host networking.
- No host port is published unless explicitly requested.

The container host administrator can still inspect and control containers; do
not describe container-only networking as protection from a privileged host.

## 2. Inspect Before Mutation

Run read-only checks first:

```bash
cat /etc/os-release
ps -p 1 -o comm=
command -v tailscale || true
command -v tailscaled || true
pgrep -a -x tailscaled || true
test -c /dev/net/tun && ls -l /dev/net/tun || true
tailscale version 2>/dev/null || true
tailscale status 2>/dev/null || true
```

If `capsh` exists, inspect capabilities:

```bash
capsh --print
```

For kernel mode, inspect the actual application network namespace:

```bash
ip -brief address
ip rule show
ip route show table all
ip -6 route show table all
```

Record the exact daemon command, socket, state path, supervisor configuration,
and current node ID and Tailscale IPs before migration. Do not dump the contents
of the state file. PIDs returned by a nested runtime are not necessarily PIDs in
the current namespace; verify the target daemon's socket and state before acting.

Do not assume the presence of `/dev/net/tun` proves `NET_ADMIN` is available.
Start the daemon and inspect its exact error when capability status is unclear.

## 3. Install Inside The Container

If Tailscale is already installed, do not reinstall it. For a supported
Debian-, Ubuntu-, RHEL-, Fedora-, CentOS-, Amazon Linux-, or openSUSE-family
container, first verify the current official installer instructions. The
official mainstream Linux command is currently:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Prefer distribution-specific official package instructions when the user does
not accept a remote shell pipeline. Do not install packages on the host.

### Kernel Mode

Prefer kernel networking when adding a node for direct inbound and outbound
tailnet traffic. Applications in the same network namespace can then use normal
`ssh`, `curl` and sockets without a proxy. Here kernel networking means a real
TUN interface and OS routing; it does not require an in-kernel WireGuard module.

1. Verify `/dev/net/tun` is accessible and effective `NET_ADMIN` is available.
   `NET_RAW` is needed for ordinary raw-socket ICMP tools. A root prompt or a
   visible device alone does not prove the necessary runtime permissions.
2. If these are missing, prepare a runtime configuration change for the exact
   target. Docker device mappings and capabilities normally require recreation;
   `docker exec`, `tailscale up`, `mknod`, or setting an environment variable
   cannot supply missing capabilities or device-cgroup access. Do not silently
   switch an explicitly requested kernel setup to userspace mode.
3. Preserve all existing application mounts, environment, networks, entrypoints
   and persistent state. Back up the runtime/supervisor configuration and record
   how to restore it. Recreate only when authorized for the target workload and
   when another recovery channel exists.
4. Start one daemon with the same persistent state directory and socket. Use
   the existing init/supervisor; do not start a second daemon beside one already
   using that state. For a directly managed `tailscaled`, specify
   `--tun=tailscale0`, without `--tun=userspace-networking`.

For an existing Docker Compose service, merge these fields into its existing
definition, keeping its verified name and image. This fragment is not permission
to create another service or container:

```yaml
services:
  existing-service:  # replace with the verified application service
    devices:
      - /dev/net/tun:/dev/net/tun
    cap_add:
      - NET_ADMIN
      - NET_RAW
    # Retain its existing persistent /var/lib/tailscale state mount.
```

If and only if the service uses the official Tailscale image's `containerboot`
entrypoint, also merge:

```yaml
environment:
  TS_USERSPACE: "false"
  TS_STATE_DIR: /var/lib/tailscale
```

For an ordinary Debian/Ubuntu application image running `tailscaled` directly,
configure the daemon arguments instead; `TS_USERSPACE=false` alone has no effect.
Persist `/var/lib/tailscale` with the existing named volume or bind mount before
recreation. Do not copy the same identity into two simultaneously running nodes.
Do not use host networking or `--privileged`. A separate Tailscale container
does not give the application kernel routes unless they explicitly share a
network namespace; do not introduce a sidecar architecture without authorization.

For LXC, use the host's runtime-specific device passthrough and device-cgroup
rules for TUN (character device 10:200), plus effective network administration
capability inside the container. Do not apply Docker flags to LXC or change host
runtime configuration without the necessary access and authorization. Inspect
the actual LXC/Proxmox configuration before proposing edits.

For a container with no supervisor and no running daemon, a temporary start is:

```bash
sudo mkdir -p /var/lib/tailscale /var/run/tailscale
sudo nohup tailscaled \
  --tun=tailscale0 \
  --state=/var/lib/tailscale/tailscaled.state \
  --socket=/var/run/tailscale/tailscaled.sock \
  >/tmp/tailscaled.log 2>&1 &
```

This manual daemon is not persistent service configuration. If startup reports
a missing TUN device or insufficient permission, inspect the exact failure and
report the runtime requirement. Do not replace requested kernel mode with a
userspace proxy merely to make status appear healthy. A normal tailnet endpoint
does not require host IP forwarding, subnet advertisements or an exit node.

### Migrate An Existing Userspace Node

1. Verify an independent management path, such as runtime console access. If
   the current SSH session is the only access path, do not stop its daemon until
   a recovery channel is available.
2. Record the existing node ID/IPs, state directory, socket, userspace flags,
   Serve configuration and supervisor/runtime definition. Preserve the state
   directory with restricted permissions and make a protected consistent backup
   during the maintenance window. Never commit or display it.
3. Prepare the TUN/capability changes above and the daemon's kernel arguments.
   For the official image set `TS_USERSPACE=false`; for a direct daemon replace
   its userspace TUN argument. Keep the same persistent state and socket.
4. Stop only the verified old daemon through its supervisor and start its
   replacement. Avoid `tailscale logout`, state deletion or a second concurrent
   daemon. Check node ID/IP continuity; authenticate only if the preserved
   identity actually requires it.
5. Validate direct traffic in both directions before retiring old proxy/Serve
   configuration. A userspace TCP Serve listener on port 22 may forward to
   loopback; kernel OpenSSH must listen on the Tailscale address or a permitted
   wildcard address. Inspect `ss -lntp`, host firewall and tailnet policy. Treat
   ordinary OpenSSH and Tailscale SSH as separate authentication choices.
6. If validation fails, use the independent channel to stop only the new
   daemon and restore the backed-up runtime/supervisor configuration and original
   userspace arguments. Reuse the preserved identity, restore any task-modified
   Serve/proxy configuration, and verify the old application path. Do not
   overwrite a healthy state file with a stale copy or delete an identity.

### Kernel Configuration Rollback

For a new installation, removal is covered in section 7. Also remove only the
TUN mapping, added capabilities, environment values, supervisor unit/arguments
and state mount introduced by this task, restoring the backed-up runtime
definition. Keep a pre-existing state volume and application data. Kernel routes
and `tailscale0` should disappear when this daemon stops; inspect them rather
than flushing unrelated system routes or firewall rules. Runtime recreation
must follow the same recovery and authorization constraints as installation.

### Userspace Mode For An Existing Container

Userspace mode requires no TUN device. Use it only when requested or accepted
as the alternative to kernel mode in an unprivileged container:

```bash
sudo mkdir -p /var/lib/tailscale /var/run/tailscale
sudo nohup tailscaled \
  --tun=userspace-networking \
  --state=/var/lib/tailscale/tailscaled.state \
  --socket=/var/run/tailscale/tailscaled.sock \
  --socks5-server=127.0.0.1:1055 \
  --outbound-http-proxy-listen=127.0.0.1:1055 \
  >/tmp/tailscaled.log 2>&1 &
```

This provides proxy-based connectivity without a transparent `tailscale0`
interface. Ordinary application sockets do not automatically use it. Kernel
mode provides OS-level routes for direct application traffic.

## 4. Authenticate Safely

For an interactive session, allow `tailscale up` to print a login URL:

```bash
sudo tailscale up --hostname=<container-name>
```

For automation, prefer an orchestrator secret or protected secret file. Do not
place an auth key in source, Compose YAML, logs, process listings, or the final
response. Use tagged and ephemeral auth where appropriate for workloads.

Verify after authentication:

```bash
sudo tailscale status
sudo tailscale ip -4
```

## 5. Connect Cluster And Container

### Cluster To Container

In kernel mode, use the container's Tailscale IP and the existing application
listener directly. Confirm its bind address, tailnet policy and container
firewall permit the exact service port. Do not publish a host port or enable
Serve merely to make ordinary SSH work.

In userspace mode, expose only the local service required by the cluster. For
an HTTP service on local port 3000:

```bash
sudo tailscale serve --bg 3000
sudo tailscale serve status
```

For raw TCP, for example local port 5432:

```bash
sudo tailscale serve --bg --tcp=5432 tcp://127.0.0.1:5432
sudo tailscale serve status
```

Replace example ports with verified service ports. Never use Funnel for this
private integration unless the user explicitly requests public Internet
exposure.

### Container To Cluster

In kernel mode, use the normal client from the application container:

```bash
ssh <peer-user>@<peer-tailscale-ip>
curl http://<peer-tailscale-ip>:<service-port>
```

Replace placeholders with verified targets. Do not infer the SSH username from
the Tailscale login identity. Test IP connectivity before treating a MagicDNS
lookup failure as a routing failure.

In userspace mode, use the local proxy and resolve MagicDNS through SOCKS when the
client supports it:

```bash
curl --proxy socks5h://127.0.0.1:1055 http://<cluster-node>:<port>
```

For applications that honor proxy variables:

```bash
export ALL_PROXY=socks5://127.0.0.1:1055
export HTTP_PROXY=http://127.0.0.1:1055
export HTTPS_PROXY=http://127.0.0.1:1055
```

Do not apply proxy variables globally without checking their effect on local
and control-plane traffic.

OpenSSH does not generally honor these proxy environment variables. For a
userspace node, use an explicit TCP proxy when the installed CLI supports it:

```bash
ssh -o 'ProxyCommand=tailscale nc %h %p' <peer-user>@<peer-tailscale-ip>
```

### Access Policy

Recommend tags and least-privilege Grants for non-human cluster and container
nodes. Grant only the required source, destination, protocol, and port. Do not
silently modify tailnet policy or create auth keys; those are separate external
state changes requiring authorization.

## 6. Validate Integration

Check all relevant evidence:

```bash
pgrep -a -x tailscaled
sudo tailscale status
sudo tailscale ip -4
sudo tailscale serve status
```

Then test the real application path from the correct side. A successful
Tailscale status alone does not prove that the application port is reachable.
For kernel mode, capture:

```bash
ip -brief address show tailscale0
ip rule show
ip route show table all
ip -6 rule show
ip -6 route show table all
tailscale ping <peer-tailscale-ip>
```

Verify `tailscale0` carries this node's address and policy routing reaches the
peer. The main route table alone is insufficient. From the application namespace
test ordinary SSH or the actual service without ProxyCommand or proxy variables;
test inbound access from an authorized peer separately. `tailscale ping` tests
the daemon path and can succeed in userspace mode, so it does not prove direct
kernel application connectivity. Verify real listeners, authentication and
firewall behavior before declaring either direction functional.
Also verify that the host is absent from the tailnet machine list when the user
can provide or authorize that view.

Record whether daemon and state survive container restart. A daemon launched
with `nohup` is temporary and does not replace a proper entrypoint, supervisor,
sidecar, or Compose definition.

For changes to reversible installation or migration instructions, validate
`install/configure -> rollback -> install/configure again` in a disposable,
authorized target, including direct application traffic at both installs.
Record the environment, commands, node identity continuity and rollback evidence
in `STATE.md`. Do not migrate or uninstall a live node merely to validate this
skill's documentation. If a suitable authenticated test target is unavailable,
mark lifecycle validation blocked and distinguish static checks from runtime
evidence.

## 7. Stop Or Uninstall

Determine the requested removal level first.

### Level A: Disconnect Only

For a dedicated node with no unrelated Serve routes, disconnect while keeping
binaries and identity state:

```bash
sudo tailscale serve reset
sudo tailscale down
```

If Serve routes predate this task, inspect and preserve them instead of resetting
them globally. To reconnect with preserved settings use `tailscale up` with any
non-default flags required by the installed CLI; restore task-managed Serve
routes from the recorded configuration.

### Level B: Uninstall Package, Preserve Identity

First perform Level A. Resolve the exact daemon process or service, then stop
only Tailscale. Use a service manager when present. Otherwise inspect before
signaling:

```bash
pgrep -a -x tailscaled
```

Use the same package manager that installed Tailscale:

```bash
sudo apt-get remove tailscale
sudo yum remove tailscale
sudo dnf remove tailscale
sudo zypper rm tailscale
```

Run only the one command matching the detected distribution. Preserve
`/var/lib/tailscale/tailscaled.state` and any mounted state volume by default.

### Level C: Complete Removal

This destroys the local node identity and a later reinstall normally receives
a new Tailscale IP. Require explicit confirmation, resolve the exact path, and
then remove only:

```text
/var/lib/tailscale/tailscaled.state
```

If a different `--state` path or external volume was used, act on that exact
verified target instead. Do not recursively delete `/var/lib/tailscale`, a
volume, or a broad directory without a separately verified reason.

Deleting the corresponding machine from the Tailscale admin console is a
separate external destructive action. Do it only when explicitly requested and
authorized.

### Removal Validation

Confirm the intended level, without treating preserved state as a failure:

```bash
command -v tailscale || true
command -v tailscaled || true
pgrep -a -x tailscaled || true
test -e /var/lib/tailscale/tailscaled.state && echo state-preserved
```

For Level A, binaries and state should remain. For Level B, binaries should be
absent and state should remain. For Level C, binaries, daemon, and the exact
state file should be absent; verify the admin-console machine record separately
if deletion was requested.
