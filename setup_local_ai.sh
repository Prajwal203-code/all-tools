#!/bin/bash

# Setup Script for Local AI Alternatives
# ======================================
# This script helps you set up local AI solutions as free alternatives to ChatGPT API

set -e  # Exit on any error

echo "🚀 Setting up Free Local AI Alternatives..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running on supported OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_header "=== 1. Installing Ollama (Recommended) ==="

if command -v ollama &> /dev/null; then
    print_status "Ollama is already installed"
else
    print_status "Installing Ollama..."
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OS" == "macos" ]]; then
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            print_warning "Homebrew not found. Please install Ollama manually from https://ollama.ai"
        fi
    fi
fi

# Start Ollama service
print_status "Starting Ollama service..."
if [[ "$OS" == "linux" ]]; then
    if command -v systemctl &> /dev/null; then
        sudo systemctl start ollama
        sudo systemctl enable ollama
    else
        ollama serve > /dev/null 2>&1 &
    fi
elif [[ "$OS" == "macos" ]]; then
    ollama serve > /dev/null 2>&1 &
fi

sleep 5  # Wait for service to start

# Download recommended models
print_status "Downloading recommended models..."

models=("llama2" "codellama" "mistral")

for model in "${models[@]}"; do
    print_status "Downloading $model..."
    if ! ollama pull "$model"; then
        print_warning "Failed to download $model. You can try downloading it later with: ollama pull $model"
    fi
done

print_header "=== 2. Installing GPT4All (Alternative) ==="

if command -v python3 &> /dev/null; then
    print_status "Installing GPT4All Python package..."
    pip3 install gpt4all
    
    # Download a small model
    print_status "Setting up GPT4All..."
    python3 -c "
from gpt4all import GPT4All
print('Downloading orca-mini model...')
model = GPT4All('orca-mini-3b-gguf2-q4_0.gguf')
print('GPT4All setup complete!')
"
else
    print_warning "Python3 not found. Please install Python to use GPT4All."
fi

print_header "=== 3. Installing Python Dependencies ==="

if [ -f "requirements.txt" ]; then
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    print_status "Installing basic dependencies..."
    pip3 install requests python-dotenv transformers torch
fi

print_header "=== 4. Creating Environment Configuration ==="

if [ ! -f ".env" ]; then
    print_status "Creating .env file for API keys..."
    cat > .env << EOF
# Free AI API Keys Configuration
# ===============================

# Hugging Face (Free tier: 1000 requests/month)
# Get your token from: https://huggingface.co/settings/tokens
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Google AI Studio (Free tier available)
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Cohere (Free tier: 100 requests/month)
# Get your API key from: https://dashboard.cohere.ai/api-keys
COHERE_API_KEY=your_cohere_api_key_here

# OpenRouter (Access to free models)
# Get your API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Local settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_LOCAL_MODEL=llama2
EOF
    print_status "Created .env file. Please add your API keys."
else
    print_status ".env file already exists"
fi

print_header "=== 5. Testing Setup ==="

print_status "Testing Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    print_status "✅ Ollama is running and accessible"
    
    # Test model
    print_status "Testing Ollama model..."
    response=$(curl -s -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d '{
            "model": "llama2",
            "prompt": "Hello",
            "stream": false
        }')
    
    if echo "$response" | grep -q "response"; then
        print_status "✅ Ollama model test successful"
    else
        print_warning "⚠️ Ollama model test failed. Try: ollama pull llama2"
    fi
else
    print_error "❌ Ollama is not accessible. Please check the installation."
fi

# Test Python setup
print_status "Testing Python setup..."
if python3 -c "import requests, json; print('✅ Python dependencies OK')" 2>/dev/null; then
    print_status "✅ Python setup successful"
else
    print_warning "⚠️ Some Python dependencies might be missing"
fi

print_header "=== Setup Complete! ==="

echo -e """
${GREEN}🎉 Free AI alternatives setup is complete!${NC}

${BLUE}What you can do now:${NC}

1. ${YELLOW}Local AI (No API keys needed):${NC}
   - Ollama: curl -X POST http://localhost:11434/api/generate -d '{"model":"llama2","prompt":"Hello"}'
   - Python: python3 implementation-examples.py

2. ${YELLOW}Free API Services (Add API keys to .env):${NC}
   - Hugging Face: 1000 requests/month free
   - Google AI Studio: Generous free tier
   - Cohere: 100 requests/month free
   - OpenRouter: Access to free models

3. ${YELLOW}Quick Start:${NC}
   - Edit .env file with your API keys
   - Run: python3 implementation-examples.py
   - Check: free-ai-api-alternatives.md for documentation

${BLUE}Useful Commands:${NC}
   - List Ollama models: ollama list
   - Download new model: ollama pull <model-name>
   - Test API: python3 implementation-examples.py

${YELLOW}Need help?${NC} Check the documentation in free-ai-api-alternatives.md
"""