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
    openssh-server \
    git \
    sudo \
    curl \
    ca-certificates \
    gnupg \
    iproute2 \
    iputils-ping \
    net-tools \
    dnsutils \
    traceroute \
    tcpdump \
    procps \
    lsof \
    vim \
    nano \
    less \
    jq \
    rsync \
    wget \
    unzip \
    zip \
    htop \
    tree \
    file \
    ripgrep \
    fd-find \
    strace \
    netcat-openbsd \
    telnet \
    python3 \
    python3-venv \
    python3-pip \
    build-essential \
    cmake \
    pkg-config \
    libssl-dev \
    libcurl4-openssl-dev \
  && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /run/sshd /etc/ssh/sshd_config.d \
 && printf '%s\n' \
    'PasswordAuthentication no' \
    'PubkeyAuthentication yes' \
    'PermitRootLogin no' \
    'AuthorizedKeysFile .ssh/authorized_keys' \
    > /etc/ssh/sshd_config.d/codex-sandbox.conf \
 && ssh-keygen -A

RUN install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
 && chmod a+r /etc/apt/keyrings/docker.asc \
 && . /etc/os-release \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian ${VERSION_CODENAME} stable" > /etc/apt/sources.list.d/docker.list \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
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

RUN npm install -g \
    @openai/codex@0.125.0 \
    @anthropic-ai/claude-code@2.1.199

ARG UID=1000
ARG GID=1000
ARG USERNAME=howard
ARG SUPPLEMENTARY_GIDS=""

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
 fi; \
 for supplementary_gid in ${SUPPLEMENTARY_GIDS}; do \
   if [ "${supplementary_gid}" = "${GID}" ]; then \
     continue; \
   fi; \
   if getent group "${supplementary_gid}" >/dev/null; then \
     supplementary_group="$(getent group "${supplementary_gid}" | cut -d: -f1)"; \
   else \
     supplementary_group="hostgrp_${supplementary_gid}"; \
     groupadd -g "${supplementary_gid}" "${supplementary_group}"; \
   fi; \
   usermod -aG "${supplementary_group}" "${USERNAME}"; \
 done; \
 usermod -aG docker "${USERNAME}" \
 && echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/${USERNAME} \
 && chmod 0440 /etc/sudoers.d/${USERNAME}

WORKDIR /workspace

EXPOSE 22

USER ${USERNAME}
