---
name: vllm-embedding-server
description: Start, debug, and verify local vLLM embedding servers on this machine, especially Qwen embedding models under /mnt/share_data_78 with the vLLM virtualenv at /tmp2/howard/venv_manager/vllm. Use when the user asks to open/start/serve an embedding model with vLLM, mentions qwen-embedding, Qwen3 embedding, first GPU/card, or needs an OpenAI-compatible /v1/embeddings endpoint.
---

# vLLM Embedding Server

Use this workflow to start local embedding models with vLLM and verify that the OpenAI-compatible embeddings API is usable.

## Defaults On This Machine

- vLLM executable: `/tmp2/howard/venv_manager/vllm/bin/vllm`
- Common model root: `/mnt/share_data_78/howard/models`
- Qwen3 embedding 8B path: `/mnt/share_data_78/howard/models/qwen3-embedding-8b`
- Qwen3 embedding 4B path: `/mnt/share_data_78/howard/models/qwen3-embedding-4b`
- Default endpoint: `http://0.0.0.0:8000`
- Default served model name for 8B: `qwen-embedding-8b`
- "first card" means GPU index `0`; use `CUDA_VISIBLE_DEVICES=0`.

Note: `/mnt/share_data_78/models` may be empty. If the user says models are under `/mnt/share_data_78/models` but nothing is there, search `/mnt/share_data_78` and `/mnt/share_data_78/howard/models` before asking.

## Preflight

1. Check GPUs and free memory:

```bash
nvidia-smi --query-gpu=index,name,memory.total,memory.free --format=csv,noheader
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader
```

2. Find the model if the exact path is unknown:

```bash
find /mnt/share_data_78 -maxdepth 4 -iname '*qwen*'
```

3. Check the target port:

```bash
ss -ltnp
```

Use another port if `8000` is already listening, unless the user explicitly wants to replace the service.

## Start Qwen Embedding 8B

This vLLM install is version `0.18.0`; it does not accept `--task embed` for `vllm serve`. Use `--convert embed`.

Foreground command for debugging:

```bash
CUDA_VISIBLE_DEVICES=0 /tmp2/howard/venv_manager/vllm/bin/vllm serve /mnt/share_data_78/howard/models/qwen3-embedding-8b --convert embed --host 0.0.0.0 --port 8000 --served-model-name qwen-embedding-8b
```

Expected startup signals:

- `Found sentence-transformers modules configuration.`
- `Resolved --runner auto to --runner pooling.`
- `Supported tasks: ['token_embed', 'embed']`
- `Starting vLLM server on http://0.0.0.0:8000`
- Route list includes `/v1/embeddings` and `/v2/embed`.

If the process exits immediately with:

```text
vllm: error: unrecognized arguments: --task embed
```

rerun with `--convert embed`.

## Background Run

Prefer a background process after the foreground command has been validated:

```bash
CUDA_VISIBLE_DEVICES=0 nohup /tmp2/howard/venv_manager/vllm/bin/vllm serve /mnt/share_data_78/howard/models/qwen3-embedding-8b --convert embed --host 0.0.0.0 --port 8000 --served-model-name qwen-embedding-8b > /tmp/qwen-embedding-8b-vllm.log 2>&1 & echo $!
```

Then check:

```bash
tail -n 120 /tmp/qwen-embedding-8b-vllm.log
ps -p <PID> -o pid,ppid,stat,etime,cmd
ss -ltnp
```

If `nohup` exits with an empty log, run the same command in the foreground to capture stderr/stdout directly, fix the flags, then retry background mode.

## Verify API

Health check:

```bash
curl -sS http://127.0.0.1:8000/health
```

Embedding request:

```bash
curl -sS http://127.0.0.1:8000/v1/embeddings \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen-embedding-8b","input":["hello world"]}'
```

The response should contain an embedding vector under `data[0].embedding`.

## Operational Notes

- Qwen3 embedding 8B used about 14.1 GiB of GPU memory during model load on an RTX 4090.
- vLLM may warn that installing `orjson` makes `/v1/embeddings` faster; do not install packages unless the user asks or approves.
- Do not kill unrelated GPU processes. If another process is on GPU 0, report it and decide whether there is still enough free memory.
- If the service was started in a foreground tool session and should persist after the turn, replace it with a background `nohup` or `setsid` process before finishing.
