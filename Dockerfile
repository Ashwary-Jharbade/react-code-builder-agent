FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files first for Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into the project environment
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Run LangGraph dev server
CMD ["langgraph", "dev", "--host", "0.0.0.0"]