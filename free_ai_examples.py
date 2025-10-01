#!/usr/bin/env python3
"""
Free AI API Alternatives to ChatGPT
This script demonstrates how to use various free AI services
"""

import requests
import json
import os
from typing import List, Dict, Optional

class FreeAIClient:
    """Unified client for multiple free AI services"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN", "")
        
    def chat_ollama(self, message: str, model: str = "llama2") -> str:
        """Use Ollama for local AI inference (100% free)"""
        try:
            response = requests.post(self.ollama_url, json={
                "model": model,
                "prompt": message,
                "stream": False
            }, timeout=30)
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error: Ollama not running. Please start Ollama and pull a model first."
                
        except requests.exceptions.ConnectionError:
            return "Error: Ollama not running. Install and start Ollama first."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_groq(self, message: str, model: str = "llama3-8b-8192") -> str:
        """Use Groq API (free tier: 14,400 requests/day)"""
        if not self.groq_api_key:
            return "Error: Please set GROQ_API_KEY environment variable"
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": message}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_huggingface(self, message: str, model: str = "microsoft/DialoGPT-medium") -> str:
        """Use Hugging Face Inference API (free tier)"""
        if not self.hf_token:
            return "Error: Please set HUGGINGFACE_TOKEN environment variable"
        
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{model}",
                headers={"Authorization": f"Bearer {self.hf_token}"},
                json={
                    "inputs": message,
                    "parameters": {
                        "max_length": 100,
                        "temperature": 0.7
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "No response generated")
                return str(result)
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat_openrouter(self, message: str, model: str = "meta-llama/llama-3.1-8b-instruct:free") -> str:
        """Use OpenRouter (many free models)"""
        api_key = os.getenv("OPENROUTER_API_KEY", "")
        if not api_key:
            return "Error: Please set OPENROUTER_API_KEY environment variable"
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": message}],
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

def demo_all_providers():
    """Demonstrate all free AI providers"""
    client = FreeAIClient()
    test_message = "Explain quantum computing in simple terms"
    
    print("🤖 Free AI Providers Demo")
    print("=" * 50)
    
    # Test Ollama (local)
    print("\n1. Ollama (Local - 100% Free)")
    print("-" * 30)
    response = client.chat_ollama(test_message)
    print(f"Response: {response[:200]}...")
    
    # Test Groq
    print("\n2. Groq (Free Tier - 14,400 requests/day)")
    print("-" * 30)
    response = client.chat_groq(test_message)
    print(f"Response: {response[:200]}...")
    
    # Test Hugging Face
    print("\n3. Hugging Face (Free Tier)")
    print("-" * 30)
    response = client.chat_huggingface(test_message)
    print(f"Response: {response[:200]}...")
    
    # Test OpenRouter
    print("\n4. OpenRouter (Free Models)")
    print("-" * 30)
    response = client.chat_openrouter(test_message)
    print(f"Response: {response[:200]}...")

def interactive_chat():
    """Interactive chat using the best available provider"""
    client = FreeAIClient()
    
    print("🤖 Interactive Free AI Chat")
    print("=" * 30)
    print("Available providers:")
    print("1. Ollama (local)")
    print("2. Groq (free tier)")
    print("3. Hugging Face (free tier)")
    print("4. OpenRouter (free models)")
    
    choice = input("\nSelect provider (1-4): ").strip()
    
    while True:
        message = input("\nYou: ").strip()
        if message.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye! 👋")
            break
        
        if not message:
            continue
        
        print("\nAI: ", end="", flush=True)
        
        if choice == "1":
            response = client.chat_ollama(message)
        elif choice == "2":
            response = client.chat_groq(message)
        elif choice == "3":
            response = client.chat_huggingface(message)
        elif choice == "4":
            response = client.chat_openrouter(message)
        else:
            print("Invalid choice. Using Ollama as default.")
            response = client.chat_ollama(message)
        
        print(response)

if __name__ == "__main__":
    print("Free AI API Alternatives")
    print("=" * 30)
    print("1. Demo all providers")
    print("2. Interactive chat")
    
    choice = input("Select option (1-2): ").strip()
    
    if choice == "1":
        demo_all_providers()
    elif choice == "2":
        interactive_chat()
    else:
        print("Invalid choice. Running demo...")
        demo_all_providers()