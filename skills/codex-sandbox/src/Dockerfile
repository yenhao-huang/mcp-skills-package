# syntax=docker/dockerfile:1.7
FROM node:20-slim

ENV VIRTUAL_ENV=/opt/python \
    PATH="/opt/python/bin:${PATH}" \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    UV_HTTP_TIMEOUT=600 \
    UV_HTTP_RETRIES=10

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    git \
    sudo \
    curl \
    ca-certificates \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev \
    libcurl4-openssl-dev \
  && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=cache,target=/root/.cache/uv \
    python3 -m venv "${VIRTUAL_ENV}" \
 && python -m pip install --upgrade pip setuptools wheel uv \
 && uv pip install --python "${VIRTUAL_ENV}/bin/python" vllm

ARG LLAMA_CPP_REF=master
RUN git clone --depth 1 --branch "${LLAMA_CPP_REF}" https://github.com/ggml-org/llama.cpp.git /tmp/llama.cpp \
 && cmake -S /tmp/llama.cpp -B /tmp/llama.cpp/build \
      -DCMAKE_BUILD_TYPE=Release \
      -DLLAMA_CURL=ON \
 && cmake --build /tmp/llama.cpp/build --target llama-server --parallel "$(nproc)" \
 && find /tmp/llama.cpp/build/bin -maxdepth 1 -type f -name "*.so*" -exec install -m 0755 {} /usr/local/lib/ \; \
 && install -m 0755 /tmp/llama.cpp/build/bin/llama-server /usr/local/bin/llama-server \
 && ldconfig \
 && rm -rf /tmp/llama.cpp

RUN npm install -g @openai/codex@0.125.0

ARG UID=1000
ARG GID=1000
ARG USERNAME=howard

RUN set -eux; \
 if ! getent group "${GID}" >/dev/null; then \
   groupadd -g "${GID}" "${USERNAME}"; \
 fi; \
 if id -u "${USERNAME}" >/dev/null 2>&1; then \
   usermod -u "${UID}" -g "${GID}" -d "/home/${USERNAME}" -m "${USERNAME}"; \
 elif getent passwd "${UID}" >/dev/null; then \
   existing_user="$(getent passwd "${UID}" | cut -d: -f1)"; \
   usermod -l "${USERNAME}" -g "${GID}" -d "/home/${USERNAME}" -m "${existing_user}"; \
 else \
   useradd -m -u "${UID}" -g "${GID}" -s /bin/bash "${USERNAME}"; \
 fi \
 && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}

WORKDIR /workspace

USER ${USERNAME}
