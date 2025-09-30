#!/usr/bin/env bash
set -euo pipefail

# Minimal curl wrapper for Hugging Face Inference API (text generation)
# Usage:
#   export HF_TOKEN=... 
#   export HF_MODEL=HuggingFaceH4/zephyr-7b-beta
#   ./scripts/hf_chat.sh "Say hi in one sentence."

if [[ -z "${HF_TOKEN:-}" ]]; then
	echo "ERROR: HF_TOKEN is required in the environment" >&2
	exit 2
fi

MODEL="${HF_MODEL:-HuggingFaceH4/zephyr-7b-beta}"

if [[ $# -lt 1 ]]; then
	echo "Usage: HF_TOKEN=... HF_MODEL=... $0 \"your prompt here\"" >&2
	exit 2
fi

PROMPT="$1"

curl -s -X POST "https://api-inference.huggingface.co/models/${MODEL}" \
	-H "Authorization: Bearer ${HF_TOKEN}" \
	-H "Content-Type: application/json" \
	-d "{\"inputs\": \"${PROMPT//\"/\\\"}\", \"parameters\": {\"max_new_tokens\": 128}}" | cat

