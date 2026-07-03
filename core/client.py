import time
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from core.image_utils import encode_image, get_media_type
from core.parsing import parse_json_response

def call_llm_api(
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: str,
    temperature: float = 1.0,
    max_tokens: int = 4096,
    reasoning_effort: str = "low",
    client: OpenAI = None,
    prompt_cache_key: str = None
) -> dict:
    """
    Sendet System-Prompt, User-Prompt und ein Bild an die LLM-API
    und gibt die strukturierte Antwort samt Metadaten zurück.
    """
    if client is None:
        client = OpenAI()

    image_b64 = encode_image(image_path)
    media_type = get_media_type(image_path)

    start_time = time.time()

    kwargs = {
        "model": model,
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
        "reasoning_effort": reasoning_effort,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{media_type};base64,{image_b64}",
                            "detail": "high",
                        },
                    },
                ],
            },
        ],
    }
    if prompt_cache_key is not None:
        kwargs["prompt_cache_key"] = prompt_cache_key

    completion = client.chat.completions.create(**kwargs)

    elapsed = time.time() - start_time
    raw_response = completion.choices[0].message.content
    parsed = parse_json_response(raw_response)

    usage = completion.usage
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    total_tokens = usage.total_tokens

    cached_tokens = 0
    if hasattr(usage, "prompt_tokens_details") and usage.prompt_tokens_details is not None:
        cached_tokens = getattr(usage.prompt_tokens_details, "cached_tokens", 0) or 0

    reasoning_tokens = 0
    if hasattr(usage, "completion_tokens_details") and usage.completion_tokens_details is not None:
        reasoning_tokens = getattr(usage.completion_tokens_details, "reasoning_tokens", 0) or 0

    uncached_tokens = max(0, prompt_tokens - cached_tokens)

    return {
        "response": parsed,
        "raw_response": raw_response,
        "metadata": {
            "model": model,
            "temperature": temperature,
            "timestamp": datetime.now().isoformat(),
            "image_name": Path(image_path).stem,
            "elapsed_seconds": round(elapsed, 2),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cached_tokens": cached_tokens,
            "uncached_tokens": uncached_tokens,
            "reasoning_tokens": reasoning_tokens,
            "json_valid": parsed is not None,
        }
    }
