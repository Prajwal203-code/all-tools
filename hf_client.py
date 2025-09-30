#!/usr/bin/env python3
"""
Minimal Hugging Face Inference API client.

Usage examples:
  1) Simple prompt
     HF_TOKEN=... HF_MODEL=HuggingFaceH4/zephyr-7b-beta python hf_client.py --prompt "Say hi in one sentence."

  2) Chat-style (system + user)
     HF_TOKEN=... python hf_client.py --model HuggingFaceH4/zephyr-7b-beta \
       --system "You are concise." --user "Explain JSON in one line."

Environment variables:
  HF_TOKEN  - Required. Your Hugging Face access token
  HF_MODEL  - Optional. Default: HuggingFaceH4/zephyr-7b-beta
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests

try:
    # Load .env if present
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    # dotenv is optional for convenience
    pass


DEFAULT_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")


def build_zephyr_chat_prompt(system: Optional[str], user: str, assistant: Optional[str] = None) -> str:
    """
    Compose a Zephyr-style prompt using special role tags.
    Compatible with many chat-tuned HF models that understand these tags.
    """
    segments: List[str] = []
    if system:
        segments.append(f"<|system|>{system}")
    segments.append(f"<|user|>{user}")
    # Providing an assistant prefix can bias the model; optional.
    if assistant:
        segments.append(f"<|assistant|>{assistant}")
    else:
        segments.append("<|assistant|>")
    return "".join(segments)


class HuggingFaceInferenceClient:
    """Thin wrapper around the Hugging Face Inference API (text generation)."""

    def __init__(self, token: str, model: str, timeout_seconds: int = 60) -> None:
        if not token:
            raise ValueError("HF_TOKEN is required. Set it in env or pass via CLI.")
        self.token = token
        self.model = model
        self.timeout_seconds = max(5, timeout_seconds)
        self.endpoint = f"https://api-inference.huggingface.co/models/{model}"
        self.session = requests.Session()

    def generate(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Call the Inference API with a raw prompt ("inputs").
        Returns the parsed JSON response.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {"inputs": prompt}
        if parameters:
            payload["parameters"] = parameters
        response = self.session.post(
            self.endpoint,
            headers=headers,
            data=json.dumps(payload),
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def chat(self, messages: List[Dict[str, str]], parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        messages: list of { role: "system"|"user"|"assistant", content: str }
        Converts to a Zephyr-style prompt and calls generate().
        """
        system_content: Optional[str] = None
        user_content: Optional[str] = None
        assistant_content: Optional[str] = None

        for message in messages:
            role = message.get("role")
            content = message.get("content", "")
            if role == "system":
                system_content = content
            elif role == "user":
                user_content = content
            elif role == "assistant":
                assistant_content = content

        if not user_content:
            raise ValueError("At least one user message is required for chat().")

        prompt = build_zephyr_chat_prompt(system_content, user_content, assistant_content)
        return self.generate(prompt, parameters=parameters)


def extract_text_from_response(response_json: Any) -> str:
    """
    HF Inference API commonly returns a list of objects with a 'generated_text' field.
    Fall back to raw JSON string if structure differs.
    """
    try:
        if isinstance(response_json, list) and len(response_json) > 0:
            first = response_json[0]
            if isinstance(first, dict) and "generated_text" in first:
                # When using chat-like prompt, the model may echo the prompt + answer.
                # We attempt to return only the completion portion when possible.
                return str(first["generated_text"])  # type: ignore[index]
        # Some endpoints may return dicts or alternative fields; stringify safely.
        return json.dumps(response_json, ensure_ascii=False)
    except Exception:
        return json.dumps(response_json, ensure_ascii=False)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hugging Face Inference API client")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model repo id (e.g., HuggingFaceH4/zephyr-7b-beta)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--prompt", help="Raw prompt string for single-shot generation")
    group.add_argument("--stdin", action="store_true", help="Read prompt from STDIN")
    # Chat-style options
    parser.add_argument("--system", help="System message for chat-style prompt")
    parser.add_argument("--user", help="User message for chat-style prompt")
    parser.add_argument("--assistant", help="Optional assistant prefix for chat-style prompt")
    # Generation parameters
    parser.add_argument("--max-tokens", type=int, default=128, help="Max new tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.7, help="Sampling temperature")
    parser.add_argument("--top-p", type=float, default=0.95, help="Nucleus sampling p")
    parser.add_argument("--seed", type=int, help="Optional random seed, if supported")
    # Output control
    parser.add_argument("--json", action="store_true", help="Print raw JSON response instead of text only")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    token = os.getenv("HF_TOKEN", "").strip()
    if not token:
        print("ERROR: HF_TOKEN is required. Set it in your environment or .env.", file=sys.stderr)
        return 2

    parameters: Dict[str, Any] = {
        "max_new_tokens": max(1, args.max_tokens),
        "temperature": max(0.0, args.temperature),
        "top_p": min(1.0, max(0.0, args.top_p)),
    }
    if args.seed is not None:
        parameters["seed"] = args.seed

    client = HuggingFaceInferenceClient(token=token, model=args.model)

    # Decide mode: raw prompt, stdin, or chat
    response: Any
    if args.prompt:
        response = client.generate(args.prompt, parameters=parameters)
    elif args.stdin:
        prompt_text = sys.stdin.read()
        response = client.generate(prompt_text, parameters=parameters)
    elif args.user or args.system or args.assistant:
        if not args.user:
            print("ERROR: --user is required when using chat-style options.", file=sys.stderr)
            return 2
        messages = []
        if args.system:
            messages.append({"role": "system", "content": args.system})
        messages.append({"role": "user", "content": args.user})
        if args.assistant:
            messages.append({"role": "assistant", "content": args.assistant})
        response = client.chat(messages, parameters=parameters)
    else:
        print("ERROR: Provide --prompt, --stdin, or chat-style flags (--user [--system] [--assistant]).", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(response, ensure_ascii=False, indent=2))
    else:
        print(extract_text_from_response(response))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

