# 🤖 Free AI API Alternatives to ChatGPT

This repository provides comprehensive solutions for replacing ChatGPT API with **completely free alternatives** that you can use in your projects without any cost limitations.

## 🎯 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Make setup script executable and run
chmod +x setup_local_ai.sh
./setup_local_ai.sh

# Start using free AI alternatives
python3 implementation-examples.py
```

### Option 2: Docker Setup
```bash
# Using Docker Compose (includes Ollama + Web UI)
docker-compose up -d

# Access Ollama Web UI at http://localhost:3000
# Your app will be at http://localhost:8080
```

### Option 3: Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run examples
python3 implementation-examples.py
node quick_start_examples.js
```

## 🆓 Available Free Alternatives

### 🏠 **Local Solutions (100% Free, No Limits)**

| Service | Installation | Models | Offline |
|---------|-------------|---------|---------|
| **Ollama** | `curl -fsSL https://ollama.ai/install.sh \| sh` | Llama 2, Mistral, CodeLlama | ✅ |
| **GPT4All** | `pip install gpt4all` | Orca, Vicuna, GPT4All-J | ✅ |
| **LM Studio** | Download from website | 1000+ models | ✅ |

### 🌐 **Free API Services**

| Service | Free Tier | Signup | Best For |
|---------|-----------|--------|----------|
| **Hugging Face** | 1,000 requests/month | [Sign up](https://huggingface.co) | Open source models |
| **Google AI Studio** | Generous free tier | [Sign up](https://makersuite.google.com) | Gemini models |
| **Cohere** | 100 requests/month | [Sign up](https://dashboard.cohere.ai) | Production ready |
| **OpenRouter** | Free models available | [Sign up](https://openrouter.ai) | Multiple models |

## 💻 Usage Examples

### Python Example
```python
from implementation_examples import UnifiedAIClient, OllamaAPI

# Local AI (no API key needed)
ollama = OllamaAPI()
response = ollama.generate("Explain quantum computing")
print(response)

# Unified client for multiple services
client = UnifiedAIClient()
client.add_service("ollama", ollama)
result = client.generate_text("Write a poem about AI", "ollama")
```

### JavaScript Example
```javascript
const { OllamaAPI, UnifiedAIClient } = require('./quick_start_examples');

// Local AI
const ollama = new OllamaAPI();
const response = await ollama.generate("What is machine learning?");
console.log(response);

// Web server
const express = require('express');
const app = createWebServer(); // Built-in web server
```

### cURL Example (Direct API)
```bash
# Ollama (local)
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama2","prompt":"Hello world","stream":false}'

# Hugging Face
curl -X POST "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs":"Hello!"}'
```

## 🚀 Advanced Features

### Switch Between Services
```python
# Automatically fallback to different services
services = ["ollama", "huggingface", "cohere"]
for service in services:
    try:
        response = client.generate_text(prompt, service)
        break
    except:
        continue
```

### Batch Processing
```python
prompts = ["Explain AI", "What is ML?", "Define neural networks"]
responses = []

for prompt in prompts:
    response = ollama.generate(prompt)
    responses.append(response)
```

### Web Integration
```javascript
// Express.js server with free AI
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    const response = await ollama.generate(message);
    res.json({ response });
});
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Free API Keys (optional)
HUGGINGFACE_TOKEN=your_token
GOOGLE_AI_API_KEY=your_key
COHERE_API_KEY=your_key
OPENROUTER_API_KEY=your_key

# Local settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama2
```

### Model Selection
```python
# Different models for different tasks
models = {
    "coding": "codellama",
    "general": "llama2", 
    "small_fast": "phi",
    "large_smart": "mixtral"
}

response = ollama.generate(prompt, model=models["coding"])
```

## 📊 Performance Comparison

| Metric | Ollama (Local) | Hugging Face | Google AI | Cohere |
|--------|---------------|--------------|-----------|---------|
| **Speed** | Fast | Medium | Fast | Fast |
| **Privacy** | 100% Private | Data processed | Data processed | Data processed |
| **Cost** | Free | Free tier | Free tier | Free tier |
| **Limits** | None | 1K/month | Generous | 100/month |
| **Quality** | High | Varies | Very High | High |

## 🛠️ Available Commands

```bash
# Setup
npm run install-local    # Install local AI tools
npm start                # Run demo
npm run server          # Start web server

# Testing
npm run test-ollama     # Test Ollama connection
npm run list-ollama     # List available models

# Python
python3 implementation-examples.py  # Run Python demo
python3 -c "from implementation_examples import *; main()"
```

## 🔍 Troubleshooting

### Ollama Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama service
ollama serve

# Download a model
ollama pull llama2

# List installed models
ollama list
```

### API Key Issues
```bash
# Test Hugging Face token
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium

# Verify .env file is loaded
node -e "require('dotenv').config(); console.log(process.env.HUGGINGFACE_TOKEN)"
```

### Common Fixes
```bash
# Fix Python dependencies
pip install --upgrade -r requirements.txt

# Fix Node.js dependencies  
npm install --force

# Reset Ollama
ollama stop && ollama start
```

## 📚 Documentation

- **[Complete API Guide](free-ai-api-alternatives.md)** - Detailed documentation
- **[Implementation Examples](implementation-examples.py)** - Python code
- **[JavaScript Examples](quick_start_examples.js)** - Node.js code
- **[Setup Script](setup_local_ai.sh)** - Automated installation

## 🎮 Interactive Examples

### Chat Interface
```python
# Simple chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    response = ollama.generate(user_input)
    print(f"AI: {response}")
```

### Web Interface
```html
<!-- Simple HTML chat -->
<script>
async function sendMessage() {
    const message = document.getElementById('message').value;
    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: message, service: 'ollama'})
    });
    const result = await response.json();
    document.getElementById('response').innerText = result.response;
}
</script>
```

## 🚀 Deployment Options

### Local Development
```bash
# Run everything locally
./setup_local_ai.sh
python3 implementation-examples.py
```

### Docker Deployment
```bash
# Full stack with Ollama
docker-compose up -d

# Just your app
docker build -t free-ai-app .
docker run -p 8080:8080 free-ai-app
```

### Cloud Deployment
```bash
# Deploy to any cloud with Docker support
# Works on: DigitalOcean, AWS, GCP, Azure, etc.
```

## 🤝 Contributing

1. Fork the repository
2. Add new free AI service integrations
3. Improve documentation
4. Submit pull requests

## 📜 License

MIT License - feel free to use in your projects!

## 🆘 Support

- 📖 Check the [documentation](free-ai-api-alternatives.md)
- 🐛 Report issues on GitHub
- 💬 Community discussions welcome

---

**🎉 You now have multiple free alternatives to ChatGPT API! No more API costs or rate limits.**