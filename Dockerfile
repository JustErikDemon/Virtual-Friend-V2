# STAGE 1: Builder
FROM python:3.12.12 AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# Create venv and install dependencies
RUN python -m venv .venv
COPY requirements.txt ./
RUN .venv/bin/pip install -r requirements.txt

# STAGE 2: Final (Slim)
FROM python:3.12.12-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv .venv/
COPY . .

# --- CRITICAL FIX START ---
# Add the virtual environment to the system PATH.
# Without this, "uvicorn" command will not be found.
ENV PATH="/app/.venv/bin:$PATH"
# --- CRITICAL FIX END ---

# Run the app on port 8080 (Required for Fly.io)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
