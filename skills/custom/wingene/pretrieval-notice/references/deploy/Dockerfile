FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends git openssh-client ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*
ARG RUN_UID=1016
ARG RUN_GID=1016
RUN groupadd --gid ${RUN_GID} runner && useradd --uid ${RUN_UID} --gid ${RUN_GID} --create-home runner
COPY references/scripts /app/references/scripts
COPY references/template/report.template.md /app/references/template/report.template.md
USER runner
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=Asia/Taipei
ENTRYPOINT ["python3", "/app/references/scripts/publish.py"]
CMD ["serve"]
