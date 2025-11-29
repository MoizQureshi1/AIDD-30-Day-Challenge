import os
import json

from dotenv import load_dotenv
import requests


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

GEMINI_API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
)


def _call_gemini(prompt: str) -> dict:
    """
    Direct HTTP call to Gemini REST API (no genai SDK).
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set in environment or .env file.")

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt,
                    }
                ]
            }
        ]
    }

    resp = requests.post(GEMINI_API_URL, headers=headers, data=json.dumps(body), timeout=60)
    resp.raise_for_status()
    return resp.json()


def _extract_text_from_response(data: dict) -> str:
    """
    Extract plain text from Gemini HTTP JSON response.
    """
    try:
        candidates = data.get("candidates") or []
        if not candidates:
            return json.dumps(data)
        c0 = candidates[0]
        content = c0.get("content") or {}
        parts = content.get("parts") or []
        if not parts:
            return json.dumps(c0)
        p0 = parts[0]
        if isinstance(p0, dict) and "text" in p0:
            return p0["text"]
        return json.dumps(p0)
    except Exception:
        return json.dumps(data)


class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        data = _call_gemini(prompt)
        return _extract_text_from_response(data)


