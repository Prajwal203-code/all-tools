## Hugging Face Inference API – Minimal Client

This project provides a minimal Python client and a curl script to call the Hugging Face Inference API using the free (rate-limited) tier.

### Prerequisites
- A free Hugging Face account and an access token: see `https://huggingface.co/settings/tokens`
- Python 3.8+

### Setup
1. Copy `.env.example` to `.env` and fill in your token:
   - `HF_TOKEN=...`
   - Optionally set `HF_MODEL` (default: `HuggingFaceH4/zephyr-7b-beta`)
2. (Optional) Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

### Quick test with curl
```bash
export HF_TOKEN=your_token
export HF_MODEL=HuggingFaceH4/zephyr-7b-beta
bash scripts/hf_chat.sh "Say hi in one sentence."
```

### Python usage
Single-shot prompt:
```bash
HF_TOKEN=your_token HF_MODEL=HuggingFaceH4/zephyr-7b-beta \
python hf_client.py --prompt "Say hi in one sentence."
```

Chat-style (system + user):
```bash
HF_TOKEN=your_token python hf_client.py \
  --model HuggingFaceH4/zephyr-7b-beta \
  --system "You are concise." \
  --user "Explain JSON in one line."
```

Read prompt from STDIN:
```bash
HF_TOKEN=your_token python hf_client.py --stdin < prompt.txt
```

Print raw JSON:
```bash
HF_TOKEN=your_token python hf_client.py --prompt "Hi" --json
```

### Notes
- Free tier is rate-limited and may queue requests; retries are not implemented here.
- For chat models, this client builds a Zephyr-style prompt with `<|system|>`, `<|user|>`, and `<|assistant|>` tags.
- You can substitute any public text-generation model you have access to (e.g., `meta-llama/Meta-Llama-3-8B-Instruct`).

