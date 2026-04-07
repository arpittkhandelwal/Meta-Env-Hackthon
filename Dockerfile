FROM python:3.10-slim

# Create a non-root user for security (HF Requirement)
RUN useradd -m -u 1000 user
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt-dir/lists/*

# Copy configuration files
COPY --chown=user pyproject.toml .
COPY --chown=user uv.lock .
COPY --chown=user requirements.txt .

# Copy source code
COPY --chown=user . .

# Switch to non-root user for installation
USER user

# Install dependencies and project
# Installing -e . ensures the 'server' script works.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Environment setup
ENV PATH="/home/user/.local/bin:$PATH"
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 7860
USER user

# Using the 'server' command defined in pyproject.toml
CMD ["server"]
