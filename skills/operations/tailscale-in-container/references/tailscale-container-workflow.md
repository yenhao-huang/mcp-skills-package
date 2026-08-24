# Tailscale Container Workflow

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

## 1. Define The Boundary

Establish all of the following before changing anything:

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

Use kernel mode only when the running container already has `/dev/net/tun` and
the required capabilities. Create narrowly scoped runtime paths, then start the
daemon using the container's existing supervisor when available. In a container
without an init system, a temporary session can use:

```bash
sudo mkdir -p /var/lib/tailscale /var/run/tailscale
sudo nohup tailscaled \
  --state=/var/lib/tailscale/tailscaled.state \
  --socket=/var/run/tailscale/tailscaled.sock \
  >/tmp/tailscaled.log 2>&1 &
```

If startup reports a missing TUN device or insufficient permission, stop and
use userspace mode. Do not claim that capabilities can be added to an already
running Docker container.

### Userspace Mode For An Existing Container

Userspace mode requires no TUN device and is the default fallback for an
already running unprivileged container:

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

This is a proxy-based path, not a transparent `tailscale0` interface. Explain
that arbitrary Layer 3 traffic and normal ICMP behavior require kernel mode and
usually container recreation with `/dev/net/tun`, `NET_ADMIN`, and `NET_RAW`.

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

Use the local userspace proxy and resolve MagicDNS through SOCKS when the
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
Also verify that the host is absent from the tailnet machine list when the user
can provide or authorize that view.

Record whether daemon and state survive container restart. A daemon launched
with `nohup` is temporary and does not replace a proper entrypoint, supervisor,
sidecar, or Compose definition.

## 7. Stop Or Uninstall

Determine the requested removal level first.

### Level A: Disconnect Only

Stop Serve routes and disconnect while keeping binaries and identity state:

```bash
sudo tailscale serve reset
sudo tailscale down
```

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
