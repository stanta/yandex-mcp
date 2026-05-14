FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    YANDEX_MCP_HTTP_HOST=0.0.0.0 \
    YANDEX_MCP_HTTP_PORT=9639 \
    YANDEX_MCP_HTTP_PATH=/mcp
WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md README.ru.md server.py ./
COPY yandex_mcp ./yandex_mcp

RUN pip install . \
    && useradd --create-home --shell /usr/sbin/nologin appuser

USER appuser

EXPOSE 9639

CMD ["yandex-mcp", "--transport", "streamable-http"]
