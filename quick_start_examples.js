// Free AI API Alternatives - JavaScript/Node.js Examples
// =====================================================

const https = require('https');
const http = require('http');

// =============================================================================
// 1. HUGGING FACE INFERENCE API
// =============================================================================

class HuggingFaceAPI {
    constructor(apiToken) {
        this.apiToken = apiToken;
        this.baseUrl = 'https://api-inference.huggingface.co/models';
    }

    async generateText(prompt, model = 'microsoft/DialoGPT-medium') {
        const url = `${this.baseUrl}/${model}`;
        const data = JSON.stringify({
            inputs: prompt,
            parameters: {
                max_length: 100,
                temperature: 0.7,
                do_sample: true
            }
        });

        const options = {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiToken}`,
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        return new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        if (Array.isArray(result) && result.length > 0) {
                            resolve(result[0].generated_text || '');
                        } else {
                            resolve(JSON.stringify(result));
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }

    async classifyText(text, model = 'cardiffnlp/twitter-roberta-base-sentiment-latest') {
        const url = `${this.baseUrl}/${model}`;
        const data = JSON.stringify({ inputs: text });

        const options = {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiToken}`,
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        return new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        resolve(JSON.parse(responseData));
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }
}

// =============================================================================
// 2. OLLAMA LOCAL API
// =============================================================================

class OllamaAPI {
    constructor(baseUrl = 'http://localhost:11434') {
        this.baseUrl = baseUrl;
    }

    async generate(prompt, model = 'llama2') {
        const url = `${this.baseUrl}/api/generate`;
        const data = JSON.stringify({
            model: model,
            prompt: prompt,
            stream: false
        });

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        return new Promise((resolve, reject) => {
            const req = http.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        resolve(result.response || '');
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }

    async chat(messages, model = 'llama2') {
        const url = `${this.baseUrl}/api/chat`;
        const data = JSON.stringify({
            model: model,
            messages: messages,
            stream: false
        });

        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };

        return new Promise((resolve, reject) => {
            const req = http.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        resolve(result.message?.content || '');
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }

    async listModels() {
        const url = `${this.baseUrl}/api/tags`;

        const options = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        return new Promise((resolve, reject) => {
            const req = http.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        resolve(result.models?.map(model => model.name) || []);
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.end();
        });
    }
}

// =============================================================================
// 3. OPENROUTER API
// =============================================================================

class OpenRouterAPI {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://openrouter.ai/api/v1';
    }

    async chatCompletion(messages, model = 'microsoft/wizardlm-2-8x22b') {
        const url = `${this.baseUrl}/chat/completions`;
        const data = JSON.stringify({
            model: model,
            messages: messages,
            temperature: 0.7,
            max_tokens: 500
        });

        const options = {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:3000',
                'X-Title': 'Free AI Assistant',
                'Content-Length': data.length
            }
        };

        return new Promise((resolve, reject) => {
            const req = https.request(url, options, (res) => {
                let responseData = '';
                res.on('data', (chunk) => responseData += chunk);
                res.on('end', () => {
                    try {
                        const result = JSON.parse(responseData);
                        if (result.choices && result.choices.length > 0) {
                            resolve(result.choices[0].message.content);
                        } else {
                            resolve('No response generated');
                        }
                    } catch (error) {
                        reject(error);
                    }
                });
            });

            req.on('error', reject);
            req.write(data);
            req.end();
        });
    }
}

// =============================================================================
// 4. UNIFIED AI CLIENT
// =============================================================================

class UnifiedAIClient {
    constructor() {
        this.services = {};
    }

    addService(name, serviceInstance) {
        this.services[name] = serviceInstance;
    }

    async generateText(prompt, service = 'ollama', options = {}) {
        if (!this.services[service]) {
            throw new Error(`Service '${service}' not available`);
        }

        const serviceInstance = this.services[service];

        try {
            switch (service) {
                case 'huggingface':
                    return await serviceInstance.generateText(prompt, options.model);
                case 'ollama':
                    return await serviceInstance.generate(prompt, options.model);
                case 'openrouter':
                    const messages = [{ role: 'user', content: prompt }];
                    return await serviceInstance.chatCompletion(messages, options.model);
                default:
                    throw new Error(`Service method not implemented for ${service}`);
            }
        } catch (error) {
            throw new Error(`Error with ${service}: ${error.message}`);
        }
    }
}

// =============================================================================
// 5. ENVIRONMENT CONFIGURATION
// =============================================================================

function loadConfig() {
    // In a real application, use dotenv or similar
    return {
        HUGGINGFACE_TOKEN: process.env.HUGGINGFACE_TOKEN,
        OPENROUTER_API_KEY: process.env.OPENROUTER_API_KEY,
        OLLAMA_BASE_URL: process.env.OLLAMA_BASE_URL || 'http://localhost:11434'
    };
}

// =============================================================================
// 6. USAGE EXAMPLES
// =============================================================================

async function demonstrateUsage() {
    console.log('🚀 Free AI API Alternatives Demo\n');

    const config = loadConfig();
    const client = new UnifiedAIClient();

    // Add available services
    if (config.HUGGINGFACE_TOKEN) {
        const hfApi = new HuggingFaceAPI(config.HUGGINGFACE_TOKEN);
        client.addService('huggingface', hfApi);
        console.log('✅ Hugging Face API configured');
    }

    if (config.OPENROUTER_API_KEY) {
        const openrouterApi = new OpenRouterAPI(config.OPENROUTER_API_KEY);
        client.addService('openrouter', openrouterApi);
        console.log('✅ OpenRouter API configured');
    }

    // Always try Ollama (local)
    try {
        const ollamaApi = new OllamaAPI(config.OLLAMA_BASE_URL);
        const models = await ollamaApi.listModels();
        if (models.length > 0) {
            client.addService('ollama', ollamaApi);
            console.log('✅ Ollama configured (local)');
            console.log(`   Available models: ${models.slice(0, 3).join(', ')}`);
        }
    } catch (error) {
        console.log('❌ Ollama not available (install and run Ollama locally)');
    }

    console.log('\n--- Testing Services ---\n');

    const prompt = 'Write a short explanation of artificial intelligence.';

    // Test each service
    for (const [serviceName, serviceInstance] of Object.entries(client.services)) {
        console.log(`\n🔍 Testing ${serviceName.toUpperCase()}:`);
        try {
            const response = await client.generateText(prompt, serviceName);
            const truncated = response.length > 200 ? response.substring(0, 200) + '...' : response;
            console.log(`Response: ${truncated}`);
        } catch (error) {
            console.log(`Error: ${error.message}`);
        }
    }
}

// =============================================================================
// 7. EXPRESS.JS WEB SERVER EXAMPLE
// =============================================================================

function createWebServer() {
    const express = require('express');
    const app = express();
    const port = 3000;

    app.use(express.json());
    app.use(express.static('public'));

    const config = loadConfig();
    const client = new UnifiedAIClient();

    // Initialize services
    if (config.HUGGINGFACE_TOKEN) {
        client.addService('huggingface', new HuggingFaceAPI(config.HUGGINGFACE_TOKEN));
    }
    if (config.OPENROUTER_API_KEY) {
        client.addService('openrouter', new OpenRouterAPI(config.OPENROUTER_API_KEY));
    }
    
    try {
        client.addService('ollama', new OllamaAPI(config.OLLAMA_BASE_URL));
    } catch (error) {
        console.log('Ollama not available');
    }

    // API endpoint for text generation
    app.post('/api/generate', async (req, res) => {
        try {
            const { prompt, service = 'ollama', model } = req.body;
            
            if (!prompt) {
                return res.status(400).json({ error: 'Prompt is required' });
            }

            const response = await client.generateText(prompt, service, { model });
            res.json({ response, service, model });
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

    // Get available services
    app.get('/api/services', (req, res) => {
        const availableServices = Object.keys(client.services);
        res.json({ services: availableServices });
    });

    app.listen(port, () => {
        console.log(`🌐 Free AI API server running at http://localhost:${port}`);
    });

    return app;
}

// =============================================================================
// 8. MAIN EXECUTION
// =============================================================================

async function main() {
    try {
        await demonstrateUsage();
    } catch (error) {
        console.error('Demo failed:', error.message);
    }
}

// Export for use in other modules
module.exports = {
    HuggingFaceAPI,
    OllamaAPI,
    OpenRouterAPI,
    UnifiedAIClient,
    createWebServer,
    main
};

// Run demo if this file is executed directly
if (require.main === module) {
    main();
}