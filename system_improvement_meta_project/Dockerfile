# Multi-stage Docker build for YAPYÖS Project Management System
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements*.txt ./
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/output /app/data

# Set permissions
RUN chmod +x otomatik_gorev_kontrolu.py

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash yapyos && \
    chown -R yapyos:yapyos /app

USER yapyos

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import json; print('OK')" || exit 1

# Default command
CMD ["python", "otomatik_gorev_kontrolu.py", "--help"]

# Development stage
FROM base as development

USER root

# Install development tools
RUN pip install pytest pytest-cov black flake8 mypy

# Install additional debugging tools
RUN apt-get update && apt-get install -y \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

USER yapyos

# Production stage  
FROM base as production

# Remove unnecessary files for production
RUN rm -rf tests/ docs/ examples/ research-journal/ \
    *.md requirements-dev.txt

# Run otomatik_gorev_kontrolu.py by default
CMD ["python", "otomatik_gorev_kontrolu.py"] 