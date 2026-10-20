FROM python:3.11-slim

WORKDIR /app

# Install system audio and networking libraries (libopus, ffmpeg for Discord voice)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopus-dev \
    libopus0 \
    ffmpeg \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY Exiters-Discord-Multi-Voice/requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create non-root user for Hugging Face Spaces compatibility
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy all project files
COPY --chown=appuser:appuser . .

USER appuser

WORKDIR /app/Exiters-Discord-Multi-Voice

# Environment defaults
ENV HOST=0.0.0.0
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

EXPOSE 7860

CMD ["python", "dashboard.py"]
