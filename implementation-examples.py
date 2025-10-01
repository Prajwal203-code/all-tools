#!/usr/bin/env python3
"""
Free AI API Implementation Examples
==================================

This file contains practical examples of how to implement free alternatives
to ChatGPT API in your Python applications.
"""

import os
import requests
import json
from typing import List, Dict, Optional

# =============================================================================
# 1. HUGGING FACE INFERENCE API EXAMPLE
# =============================================================================

class HuggingFaceAPI:
    """Free alternative using Hugging Face Inference API"""
    
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {"Authorization": f"Bearer {api_token}"}
    
    def generate_text(self, prompt: str, model: str = "microsoft/DialoGPT-medium") -> str:
        """Generate text using Hugging Face models"""
        url = f"{self.base_url}/{model}"
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 100,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return str(result)
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def classify_text(self, text: str, model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest") -> Dict:
        """Classify text sentiment using Hugging Face"""
        url = f"{self.base_url}/{model}"
        payload = {"inputs": text}
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Example usage:
# hf_api = HuggingFaceAPI("your_hugging_face_token")
# result = hf_api.generate_text("Hello, how are you today?")
# sentiment = hf_api.classify_text("I love this product!")

# =============================================================================
# 2. GOOGLE AI STUDIO (GEMINI) EXAMPLE
# =============================================================================

class GeminiAPI:
    """Free alternative using Google's Gemini via AI Studio"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def generate_content(self, prompt: str, model: str = "gemini-pro") -> str:
        """Generate content using Gemini"""
        url = f"{self.base_url}/{model}:generateContent"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(
                f"{url}?key={self.api_key}", 
                headers=headers, 
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            if "candidates" in result and len(result["candidates"]) > 0:
                content = result["candidates"][0]["content"]["parts"][0]["text"]
                return content
            return "No response generated"
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

# Example usage:
# gemini_api = GeminiAPI("your_google_ai_api_key")
# response = gemini_api.generate_content("Write a short poem about technology")

# =============================================================================
# 3. COHERE API EXAMPLE
# =============================================================================

class CohereAPI:
    """Free alternative using Cohere API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cohere.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_text(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate text using Cohere"""
        url = f"{self.base_url}/generate"
        payload = {
            "model": "command",
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if "generations" in result and len(result["generations"]) > 0:
                return result["generations"][0]["text"]
            return "No response generated"
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using Cohere"""
        url = f"{self.base_url}/embed"
        payload = {
            "texts": texts,
            "model": "embed-english-v2.0"
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("embeddings", [])
            
        except requests.exceptions.RequestException as e:
            return []

# Example usage:
# cohere_api = CohereAPI("your_cohere_api_key")
# text = cohere_api.generate_text("The future of AI is")
# embeddings = cohere_api.embed_text(["Hello world", "AI is amazing"])

# =============================================================================
# 4. OPENROUTER API EXAMPLE
# =============================================================================

class OpenRouterAPI:
    """Access multiple free models via OpenRouter"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",  # Replace with your site
            "X-Title": "Free AI Assistant"  # Replace with your app name
        }
    
    def chat_completion(self, messages: List[Dict], model: str = "microsoft/wizardlm-2-8x22b") -> str:
        """Chat completion using free models on OpenRouter"""
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            return "No response generated"
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def get_available_models(self) -> List[Dict]:
        """Get list of available models"""
        url = f"{self.base_url}/models"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            return result.get("data", [])
            
        except requests.exceptions.RequestException as e:
            return []

# Example usage:
# openrouter_api = OpenRouterAPI("your_openrouter_api_key")
# messages = [{"role": "user", "content": "Hello, how can you help me?"}]
# response = openrouter_api.chat_completion(messages)
# models = openrouter_api.get_available_models()

# =============================================================================
# 5. OLLAMA LOCAL API EXAMPLE
# =============================================================================

class OllamaAPI:
    """Local AI using Ollama"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, prompt: str, model: str = "llama2") -> str:
        """Generate text using local Ollama model"""
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "llama2") -> str:
        """Chat with local Ollama model"""
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("message", {}).get("content", "")
            
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def list_models(self) -> List[str]:
        """List available local models"""
        url = f"{self.base_url}/api/tags"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            return [model["name"] for model in result.get("models", [])]
            
        except requests.exceptions.RequestException as e:
            return []

# Example usage:
# ollama_api = OllamaAPI()
# response = ollama_api.generate("What is the meaning of life?")
# chat_response = ollama_api.chat([{"role": "user", "content": "Hello!"}])
# models = ollama_api.list_models()

# =============================================================================
# 6. UNIFIED AI CLIENT - SWITCH BETWEEN SERVICES
# =============================================================================

class UnifiedAIClient:
    """Unified client that can switch between different free AI services"""
    
    def __init__(self):
        self.services = {}
    
    def add_service(self, name: str, service_instance):
        """Add a service to the client"""
        self.services[name] = service_instance
    
    def generate_text(self, prompt: str, service: str = "huggingface", **kwargs) -> str:
        """Generate text using specified service"""
        if service not in self.services:
            return f"Service '{service}' not available"
        
        service_instance = self.services[service]
        
        try:
            if service == "huggingface":
                return service_instance.generate_text(prompt, **kwargs)
            elif service == "gemini":
                return service_instance.generate_content(prompt, **kwargs)
            elif service == "cohere":
                return service_instance.generate_text(prompt, **kwargs)
            elif service == "openrouter":
                messages = [{"role": "user", "content": prompt}]
                return service_instance.chat_completion(messages, **kwargs)
            elif service == "ollama":
                return service_instance.generate(prompt, **kwargs)
            else:
                return "Service method not implemented"
                
        except Exception as e:
            return f"Error with {service}: {str(e)}"

# =============================================================================
# 7. ENVIRONMENT CONFIGURATION
# =============================================================================

def setup_environment():
    """Setup environment variables for API keys"""
    config = {
        "HUGGINGFACE_TOKEN": os.getenv("HUGGINGFACE_TOKEN"),
        "GOOGLE_AI_API_KEY": os.getenv("GOOGLE_AI_API_KEY"),
        "COHERE_API_KEY": os.getenv("COHERE_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    }
    
    missing_keys = [key for key, value in config.items() if not value]
    if missing_keys:
        print(f"Warning: Missing environment variables: {', '.join(missing_keys)}")
    
    return config

# =============================================================================
# 8. MAIN EXAMPLE USAGE
# =============================================================================

def main():
    """Main function demonstrating usage of free AI alternatives"""
    
    # Setup environment
    config = setup_environment()
    
    # Initialize services
    client = UnifiedAIClient()
    
    # Add services that have API keys
    if config["HUGGINGFACE_TOKEN"]:
        hf_api = HuggingFaceAPI(config["HUGGINGFACE_TOKEN"])
        client.add_service("huggingface", hf_api)
    
    if config["GOOGLE_AI_API_KEY"]:
        gemini_api = GeminiAPI(config["GOOGLE_AI_API_KEY"])
        client.add_service("gemini", gemini_api)
    
    if config["COHERE_API_KEY"]:
        cohere_api = CohereAPI(config["COHERE_API_KEY"])
        client.add_service("cohere", cohere_api)
    
    if config["OPENROUTER_API_KEY"]:
        openrouter_api = OpenRouterAPI(config["OPENROUTER_API_KEY"])
        client.add_service("openrouter", openrouter_api)
    
    # Always try to add Ollama (local)
    try:
        ollama_api = OllamaAPI()
        # Test if Ollama is running
        ollama_api.list_models()
        client.add_service("ollama", ollama_api)
        print("✅ Ollama service available (local)")
    except:
        print("❌ Ollama service not available (install and run Ollama locally)")
    
    # Test prompt
    prompt = "Write a short explanation of artificial intelligence."
    
    # Try each available service
    for service_name in client.services.keys():
        print(f"\n--- Testing {service_name.upper()} ---")
        response = client.generate_text(prompt, service_name)
        print(f"Response: {response[:200]}..." if len(response) > 200 else response)

if __name__ == "__main__":
    main()