# Этап 1: установка Python + зависимостей через uv
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python
ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.12

WORKDIR /app

# Кэширование зависимостей
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

# Копируем весь код проекта
ADD .. /app

# Устанавливаем проект (бот) в окружение
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Этап 3: финальный контейнер для запуска бота
FROM debian:bookworm-slim AS runner

# Копируем Python окружение и ffmpeg
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=python:python /app /app

WORKDIR /app

# Устанавливаем libmp3lame для работы ffmpeg
RUN apt update && apt install -y libmp3lame0 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем переменные окружения
ENV PATH="/app/.venv/bin:/usr/local/bin:$PATH" \
    PYTHONPATH=/app

# Команда запуска aiogram-бота
CMD ["python", "bot/main.py"]
