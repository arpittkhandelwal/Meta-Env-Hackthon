FROM python:3.10-slim

# Create a non-root user for security (HF Requirement)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install dependencies as the non-root user
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

ENV PYTHONPATH=/app

# HF Space port
EXPOSE 7860

# Run the FastAPI app using uvicorn
CMD ["python", "app.py"]
