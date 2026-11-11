# vLLM + Nsight Systems (nsys) + Nsight Compute (ncu)
FROM vllm/vllm-openai:v0.32.0-cu129

# The base image already has the NVIDIA CUDA apt repo (ubuntu2404/sbsa) configured.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      nsight-systems-2026.5.2 \
      nsight-compute-2026.3.1 \
 && rm -rf /var/lib/apt/lists/*

ENV PATH=/opt/nvidia/nsight-systems/2026.5.2/bin:/opt/nvidia/nsight-compute/2026.3.1:$PATH

WORKDIR /work
ENTRYPOINT []
CMD ["sleep", "infinity"]
