FROM python:3.14-slim

WORKDIR /app


RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

RUN pip install  uv


COPY --chown=appuser:appuser pyproject.toml .
COPY --chown=appuser:appuser uv.lock* .

USER appuser

#ENV PYTHONDONTWRITEBYTECODE=1 \
   # PYTHONUNBUFFERED=1 \
   # PATH="/root/.local/bin:$PATH"

#RUN apt-get update \
   # && apt-get install -y --no-install-recommends curl \
  #  && rm -rf /var/lib/apt/lists/*


RUN uv sync --frozen --no-dev
#COPY --chown=appuser:appuser app/ app/
COPY --chown=appuser:appuser . .

#COPY pyproject.toml README.md ./



FROM python:3.14-slim

WORKDIR /app

RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app

RUN pip install uv

COPY --chown=appuser:appuser pyproject.toml .
COPY --chown=appuser:appuser uv.lock .

USER appuser

RUN uv sync --frozen --no-dev

COPY --chown=appuser:appuser . .

EXPOSE 8000

#HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

#CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]