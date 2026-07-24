import requests
import json
from typing import List, Dict, Generator, Any
from ..config import load_config

def _prepare_payload(messages: List[Dict[str, str]], stream: bool = False, tools: List[Dict] = None) -> Dict[str, Any]:
    cfg = load_config()
    payload = {
        "model": cfg.get("model", "qwen3.6:27b"),
        "messages": messages,
        "stream": stream,
        "temperature": 0.7,
        "max_tokens": 4096,
    }
    if tools:
        payload["tools"] = tools
    return payload

def _headers() -> Dict[str, str]:
    cfg = load_config()
    return {
        "Authorization": f"Bearer {cfg.get('api_key', '')}",
        "Content-Type": "application/json",
    }

def chat(messages: List[Dict[str, str]], stream: bool = False, tools: List[Dict] = None) -> Any:
    """Send chat messages to RCAC GenAI API.
    If stream=True, returns a generator yielding streamed JSON chunks.
    Otherwise returns the full response JSON.
    """
    cfg = load_config()
    url = cfg.get("base_url", "https://genai.rcac.purdue.edu").rstrip('/') + cfg.get("endpoint", "/api/chat/completions")
    payload = _prepare_payload(messages, stream, tools)
    response = requests.post(url, headers=_headers(), json=payload, stream=stream, timeout=60)
    
    if response.status_code == 401:
        raise RuntimeError("Unauthorized (401): Your API key is invalid or expired. Run 'rcac set-key <your-api-key>' to set a valid key.")
        
    response.raise_for_status()
    if stream:
        # iterate over SSE stream
        for line in response.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    yield json.loads(data_str)
                except json.JSONDecodeError:
                    continue
    else:
        return response.json()
