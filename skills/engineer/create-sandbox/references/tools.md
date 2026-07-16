# Create Sandbox Tooling Reference

Use this reference when updating `src/Dockerfile`, reviewing installed tools, or
deciding which utility belongs in the sandbox image. Tools listed here should be
installed by the Dockerfile unless explicitly noted as language/runtime tools.

## Core Development

Baseline tools for source checkout, privileged setup, downloads, and
certificate/key management.

```text
git
sudo
curl
wget
ca-certificates
gnupg
```

## Editors And Text Workflow

Tools for in-container edits, paged output, JSON inspection, and fast source
navigation.

```text
vim
nano
less
jq
ripgrep          # rg
fd-find          # fdfind; Dockerfile also symlinks fd
tree
file
```

## Transfer And Archives

Tools for moving files and handling common archive formats.

```text
rsync
unzip
zip
```

## Python And Native Builds

Tools for Python virtual environments, package installation, and compiling
native dependencies such as `llama.cpp`.

```text
python3
python3-venv
python3-pip
build-essential
cmake
pkg-config
libssl-dev
libcurl4-openssl-dev
```

## SSH

Tools for outbound Git SSH operations and the sandbox's SSH server.

```text
openssh-client
openssh-server
```

## Docker Engine

Tools for the privileged Docker-in-Docker daemon and its clients. The daemon
uses an internal Unix socket and does not use the host Docker socket.

```text
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
```

## Network Diagnostics

Tools for route inspection, DNS checks, connectivity tests, socket inspection,
packet capture, and process/socket correlation.

```text
iproute2          # ip, ss
iputils-ping      # ping
net-tools         # ifconfig, route, netstat
dnsutils          # dig, nslookup
traceroute
tcpdump
netcat-openbsd    # nc
telnet
lsof
```

## System Debugging

Tools for process/resource observation and low-level debugging.

```text
procps            # ps, top, free
htop
strace
```

## Project Runtime Tools

These are installed through language/package tooling rather than apt.

```text
@openai/codex
@anthropic-ai/claude-code
uv
vllm
llama-server
```

## Notes

- Debian's `fd-find` package installs `fdfind`; the Dockerfile should create a
  `/usr/local/bin/fd` symlink for the common command name.
- After editing Dockerfile package lists, update this reference so it remains a
  quick index of what the image includes.
