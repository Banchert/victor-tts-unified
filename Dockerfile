# VICTOR-TTS UNIFIED Docker Image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libportaudio2 \
    libasound2-dev \
    portaudio19-dev \
    python3-dev \
    gcc \
    g++ \
    make \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/storage/output /app/storage/temp /app/models /app/logs

# Set permissions
RUN chmod +x start.py

# Expose ports
EXPOSE 6969 7000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:6969/health || exit 1

# Default command
CMD ["python", "start.py", "--api", "--host", "0.0.0.0", "--port", "6969"] 