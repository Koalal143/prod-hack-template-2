FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ARG MODE=prod
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    MODE=$MODE


WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    if [ "$MODE" = "dev" ]; then \
          uv sync --locked --no-install-project --group dev; \
    elif [ "$MODE" = "test" ]; then \
        uv sync --locked --no-install-project --group test --no-dev; \
    elif [ "$MODE" = "prod" ]; then \
        uv sync --locked --no-install-project --no-dev; \
    else \
        echo "Unknown MODE=$MODE" >&2; exit 1; \
    fi
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$MODE" = "dev" ]; then \
        uv sync --frozen --group dev; \
    elif [ "$MODE" = "test" ]; then \
        uv sync --frozen --group test --no-dev; \
    elif [ "$MODE" = "prod" ]; then \
        uv sync --frozen --no-dev; \
    else \
        echo "Unknown MODE=$MODE" >&2; exit 1; \
    fi  


FROM python:3.12-slim-bookworm

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app/ /app/

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

EXPOSE 8000

CMD alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000