---
name: vllm-embedding-server
description: >
  Start, debug, and verify local vLLM embedding servers on this machine,
  especially Qwen embedding models under `/mnt/share_data_78` with the vLLM
  virtualenv at `/tmp2/howard/venv_manager/vllm`. Use when the user asks to
  open/start/serve an embedding model with vLLM, mentions qwen-embedding,
  Qwen3 embedding, first GPU/card, or needs an OpenAI-compatible
  `/v1/embeddings` endpoint.
---

# vLLM Embedding Server

Use this skill to start local embedding models with vLLM and verify the
OpenAI-compatible embeddings API.

## When To Use

Use this skill when the user asks to:

- Start, open, serve, debug, or verify a vLLM embedding server.
- Serve Qwen3 embedding 8B or 4B models.
- Use the first GPU/card for an embedding server.
- Expose or test an OpenAI-compatible `/v1/embeddings` endpoint.

Do not use this skill when:

- The request is about non-embedding vLLM generation unless the user explicitly
  asks to adapt these notes.
- The user wants package installation without approving environment changes.
- Another service already owns the requested port and the user has not approved
  replacing it.

## Workflow

1. Check GPUs and free memory with `nvidia-smi`.
2. Resolve the model path. If `/mnt/share_data_78/models` is empty, search
   `/mnt/share_data_78` and `/mnt/share_data_78/howard/models` before asking.
3. Check the target port with `ss -ltnp`; use another port if `8000` is busy
   unless the user explicitly wants to replace the service.
4. Run the foreground vLLM command first when debugging flags or startup.
5. After foreground startup is validated, switch to background `nohup` if the
   service should persist beyond the turn.
6. Verify `/health` and `/v1/embeddings`.
7. Report endpoint, PID/log path when backgrounded, validation result, and any
   GPU/port caveat.

## References

- vLLM executable: `/tmp2/howard/venv_manager/vllm/bin/vllm`.
- Common model root: `/mnt/share_data_78/howard/models`.
- Qwen3 embedding 8B:
  `/mnt/share_data_78/howard/models/qwen3-embedding-8b`.
- Qwen3 embedding 4B:
  `/mnt/share_data_78/howard/models/qwen3-embedding-4b`.
- Default endpoint: `http://0.0.0.0:8000`.
- Default served model name for 8B: `qwen-embedding-8b`.
- "first card" means GPU index `0`; use `CUDA_VISIBLE_DEVICES=0`.

## Environment

- This vLLM install is version `0.18.0`.
- Use `--convert embed` for `vllm serve`; do not use unsupported
  `--task embed`.
- Qwen3 embedding 8B used about 14.1 GiB of GPU memory during model load on an
  RTX 4090.

## Rules

- Do not install packages unless the user asks or approves.
- Do not kill unrelated GPU processes. If another process is on GPU 0, report it
  and decide whether enough memory remains.
- If `nohup` exits with an empty log, rerun the same command in the foreground to
  capture stderr/stdout directly.
- If a foreground tool session starts a service that should persist after the
  turn, replace it with a background `nohup` or `setsid` process before
  finishing.

## Commands

Preflight:

```bash
nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv,noheader
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader
find /mnt/share_data_78 -maxdepth 4 -iname '*qwen*'
ss -ltnp
```

Foreground 8B server:

```bash
CUDA_VISIBLE_DEVICES=0 /tmp2/howard/venv_manager/vllm/bin/vllm serve /mnt/share_data_78/howard/models/qwen3-embedding-8b --convert embed --host 0.0.0.0 --port 8000 --served-model-name qwen-embedding-8b
```

Background 8B server:

```bash
CUDA_VISIBLE_DEVICES=0 nohup /tmp2/howard/venv_manager/vllm/bin/vllm serve /mnt/share_data_78/howard/models/qwen3-embedding-8b --convert embed --host 0.0.0.0 --port 8000 --served-model-name qwen-embedding-8b > /tmp/qwen-embedding-8b-vllm.log 2>&1 & echo $!
```

Verify:

```bash
curl -sS http://127.0.0.1:8000/health
curl -sS http://127.0.0.1:8000/v1/embeddings \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen-embedding-8b","input":["hello world"]}'
```

## Output

Final responses should include:

- Endpoint and served model name.
- Whether the process is foreground or background.
- PID and log path for background runs.
- Health and embeddings validation result.
- Any GPU memory, port, or environment blocker.
