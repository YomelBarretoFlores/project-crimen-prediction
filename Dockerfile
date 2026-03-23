

FROM python:3.13-slim AS builder

WORKDIR /app


COPY pyproject.toml ./


RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .



FROM python:3.13-slim AS runtime

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/
COPY models/ ./models/


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


EXPOSE 8000


CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
