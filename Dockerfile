# ─────────────────────────────────────────────
# Stage 1: Builder
# Install dependencies in an isolated layer
# ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies into a prefix
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# ─────────────────────────────────────────────
# Stage 2: Production
# Lean final image — no build tools, no cache
# ─────────────────────────────────────────────
FROM python:3.11-slim AS production

# Security: run as non-root user
RUN groupadd -r healthcare && useradd -r -g healthcare healthcare

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/
COPY run.py .

# Create directory for SQLite database and set permissions
RUN mkdir -p /app/instance && \
    chown -R healthcare:healthcare /app

# Switch to non-root user
USER healthcare

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Use gunicorn for production (not Flask dev server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "run:app"]