# ==================== BUILD STAGE ====================
FROM python:3.13.11-slim-bookworm AS builder

# Build dependencies (compilers, dev libs)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /wheels

# Create wheel packages from requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /tmp/requirements.txt && \
    rm -rf /tmp/requirements.txt

# ==================== RUNTIME STAGE ====================
FROM python:3.13.11-slim-bookworm

# Runtime dependencies only (no compilers)
RUN apt-get update && apt-get install -y \
    libpq5 \
    gettext && \
    rm -rf /var/lib/apt/lists/*

# Copy and install pre-built wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels

# Create non-root user for security
RUN adduser --disabled-password --gecos "" app-user

# Set working directory
WORKDIR /wselfedu

# Copy project code
COPY wselfedu/ wselfedu/
COPY apps/ apps/
COPY templates/ templates/
COPY static_src/ static_src/
COPY locale/ locale/
COPY di/ di/
COPY utils/ utils/
COPY manage.py manage.py

# Compile locale translations
RUN django-admin compilemessages -l ru -l nl -l en

# Create necessary directories
RUN mkdir -p static media

# Change the owner of all files to app-user
RUN chown -R app-user:app-user .

# Switch to non-root user
USER app-user