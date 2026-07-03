---
name: send-to-vdi
description: >
  Use when the user asks to send, upload, copy, or transfer a file to VDI using send_to_vdi,
  including requests mentioning VDI, send_to_vdi, 192.168.1.2, Projects專案, !AI專區,
  or the fixed VDI image folder. This skill forbids remote-side operations on VDI and
  requires file transfer through send_to_vdi.
---

# Send To VDI

## Required Behavior

When this skill triggers, transfer files only through:

```bash
send_to_vdi <argument>
```

`<argument>` must come from the user's request. It is usually a file path, filename, or explicit argument string the user wants passed to `send_to_vdi`.

Local commands are allowed when needed to prepare or identify the file, such as creating a requested small test file, checking that a local file exists, or invoking an interactive shell so the `send_to_vdi` function is available.

## Remote Restrictions

Do not operate commands on the VDI or remote SMB share except through `send_to_vdi`.

Forbidden remote-side examples include:

- Do not use `ssh` to run commands on VDI.
- Do not use direct `smbclient` commands to browse, list, create, delete, rename, move, chmod, or inspect files on the remote share.
- Do not create remote directories.
- Do not delete, rename, move, or chmod remote files.
- Do not start a remote service or server.
- Do not validate the remote folder before or after transfer by running remote commands.
- Do not replace `send_to_vdi` with `scp`, `rsync`, `curl`, direct `smbclient`, HTTP server transfer, or any other transfer path.

## Missing Argument

If the user asks to send something but does not provide the argument to pass to `send_to_vdi`, ask for the exact argument unless the user also asked you to create the file locally.

## Quoting

If the provided argument contains spaces, shell metacharacters, or non-ASCII text, quote it safely while still running only `send_to_vdi <argument>`.

Examples:

```bash
send_to_vdi /tmp2/howard/file.tar.gz
send_to_vdi './file with spaces.tar.gz'
```

## Failure Handling

If `send_to_vdi <argument>` fails, local diagnosis is allowed. Do not run remote-side commands or use an alternate transfer method unless the user explicitly changes the instruction.
