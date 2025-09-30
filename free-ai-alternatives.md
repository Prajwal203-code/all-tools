# Free AI API Alternatives to ChatGPT

## 1. Ollama (Local Models) - 100% Free

### Installation
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download models
ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama pull phi3
```

### Usage Examples

#### Python Integration
```python
import requests
import json

def ask_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    return response.json()["response"]

# Example usage
response = ask_ollama("Explain quantum computing in simple terms")
print(response)
```

#### JavaScript Integration
```javascript
async function askOllama(prompt, model = "llama2") {
    const response = await fetch("http://localhost:11434/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            model: model,
            prompt: prompt,
            stream: false
        })
    });
    
    const data = await response.json();
    return data.response;
}

// Example usage
askOllama("Write a Python function to sort a list")
    .then(response => console.log(response));
```

## 2. Hugging Face Transformers - Free

### Installation
```bash
pip install transformers torch
```

### Usage
```python
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Text generation
generator = pipeline('text-generation', model='gpt2')
result = generator("The future of AI is", max_length=100, num_return_sequences=1)

# Chat completion
def chat_completion(messages):
    model_name = "microsoft/DialoGPT-medium"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Process conversation
    inputs = tokenizer.encode(messages, return_tensors='pt')
    outputs = model.generate(inputs, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## 3. Groq API - Free Tier

### Setup
```python
import groq

client = groq.Groq(api_key="your-groq-api-key")

def groq_chat(messages):
    response = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",  # Free model
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

## 4. OpenRouter - Multiple Free Models

### Setup
```python
import openai

# Configure for OpenRouter
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "your-openrouter-key"

def openrouter_chat(messages, model="meta-llama/llama-3.1-8b-instruct:free"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content
```

## 5. Together AI - Free Credits

### Setup
```python
import together

together.api_key = "your-together-api-key"

def together_chat(messages):
    response = together.ChatCompletion.create(
        model="meta-llama/Llama-2-7b-chat-hf",
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content
```

## Comparison Table

| Service | Cost | Speed | Privacy | Models Available |
|---------|------|-------|---------|------------------|
| Ollama | Free | Medium | 100% Private | Llama, Mistral, CodeLlama |
| Hugging Face | Free | Slow | Private | GPT-2, DialoGPT, etc. |
| Groq | Free Tier | Very Fast | API | Llama, Mistral, Mixtral |
| OpenRouter | Free Models | Fast | API | Multiple models |
| Together AI | Free Credits | Fast | API | Llama, Mistral, etc. |

## Recommended Implementation Strategy

1. **For Development/Testing**: Use Ollama locally
2. **For Production (Low Volume)**: Use Groq free tier
3. **For Production (High Volume)**: Use OpenRouter with free models
4. **For Privacy-Critical Apps**: Use Ollama or Hugging Face

## Migration from ChatGPT API

If you're currently using ChatGPT API, here's how to migrate:

```python
# Original ChatGPT API
import openai
openai.api_key = "your-openai-key"

def chatgpt_call(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Migrate to Ollama
def ollama_call(messages):
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    return ask_ollama(prompt)

# Migrate to Groq
def groq_call(messages):
    return groq_chat(messages)
```

## Best Practices

1. **Start with Ollama** for development
2. **Use multiple providers** for redundancy
3. **Implement fallback mechanisms**
4. **Monitor usage limits** for free tiers
5. **Cache responses** to reduce API calls