#!/bin/bash

echo "🚀 Setting up Free AI Alternatives to ChatGPT"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Ollama (Local AI)
echo "📦 Installing Ollama (Local AI Models)..."
if ! command_exists ollama; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "✅ Ollama installed successfully!"
else
    echo "✅ Ollama already installed"
fi

# Start Ollama service
echo "🔄 Starting Ollama service..."
ollama serve &
sleep 5

# Download popular models
echo "📥 Downloading AI models..."
echo "This may take a while depending on your internet connection..."

echo "Downloading Llama 2 (7B parameters)..."
ollama pull llama2

echo "Downloading Code Llama (for coding assistance)..."
ollama pull codellama

echo "Downloading Mistral (efficient model)..."
ollama pull mistral

echo "Downloading Phi-3 (Microsoft's efficient model)..."
ollama pull phi3

echo "✅ Models downloaded successfully!"

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install requests transformers torch

# Create environment file template
echo "📝 Creating environment file template..."
cat > .env.template << EOF
# Free AI API Keys (Optional - for cloud services)
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Get free API keys from:
# Groq: https://console.groq.com/
# Hugging Face: https://huggingface.co/settings/tokens
# OpenRouter: https://openrouter.ai/
EOF

echo "✅ Setup complete!"
echo ""
echo "🎉 You now have access to free AI alternatives:"
echo ""
echo "1. 🏠 Ollama (Local - 100% Free)"
echo "   - Run: ollama run llama2"
echo "   - Or use the Python script: python free_ai_examples.py"
echo ""
echo "2. 🌐 Web Interface"
echo "   - Open: ai-chat-app.html in your browser"
echo ""
echo "3. 🔑 Optional: Get free API keys for cloud services"
echo "   - Copy .env.template to .env and add your keys"
echo ""
echo "📚 Documentation: free-ai-alternatives.md"
echo ""
echo "Happy coding! 🚀"