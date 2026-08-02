FROM python:3.11-slim

# Avoid creating .pyc files and enable stdout/stderr to be unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps and Python deps
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Expose port (Fly provides PORT env at runtime). Default to 8000 for local testing
EXPOSE 8000
ENV PORT=8000

# Use environment PORT if provided by the platform
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
