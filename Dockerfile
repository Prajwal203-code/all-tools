# Dockerfile for Free AI Alternatives App
# ========================================

FROM node:18-slim

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install Node.js dependencies
RUN npm install

# Copy Python requirements and install
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/models /app/logs

# Set environment variables
ENV NODE_ENV=production
ENV PYTHONPATH=/app
ENV OLLAMA_BASE_URL=http://ollama:11434

# Expose ports
EXPOSE 8080
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Free AI Alternatives App..."\n\
echo "Checking Ollama connectivity..."\n\
until curl -s $OLLAMA_BASE_URL/api/tags > /dev/null; do\n\
    echo "Waiting for Ollama..."\n\
    sleep 2\n\
done\n\
echo "✅ Ollama is ready!"\n\
echo "Starting application..."\n\
node quick_start_examples.js' > /app/start.sh && chmod +x /app/start.sh

# Start command
CMD ["/app/start.sh"]