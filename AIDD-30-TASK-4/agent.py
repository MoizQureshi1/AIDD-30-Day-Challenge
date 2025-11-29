import os
import json

from dotenv import load_dotenv
import requests


load_dotenv()


def _get_api_key() -> str | None:
    """Get API key from multiple sources: env vars, Streamlit secrets, or .env file."""
    # Try environment variable first
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
    
    # Try Streamlit secrets (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass
    
    return None


def _get_model_name() -> str:
    """Get model name from multiple sources."""
    model = os.getenv("MODEL_NAME")
    if model:
        return model
    
    try:
        import streamlit as st
        model = st.secrets.get("MODEL_NAME")
        if model:
            return model
    except Exception:
        pass
    
    return "gemini-2.0-flash"


GEMINI_API_KEY = _get_api_key()
MODEL_NAME = _get_model_name()


def _call_gemini(prompt: str) -> dict:
    """
    Direct HTTP call to Gemini REST API (no genai SDK).
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Set it in environment variables, "
            "Streamlit secrets (for Cloud), or .env file (for local)."
        )
    
    model_name = _get_model_name()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
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

    resp = requests.post(api_url, headers=headers, data=json.dumps(body), timeout=60)
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


