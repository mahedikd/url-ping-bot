FROM python:3.12.11-slim-bookworm AS builder

RUN pip install uv
WORKDIR /app
COPY . /app
RUN uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"
RUN prisma generate

CMD ["sh", "-c", "prisma db push && uv run main.py"]

