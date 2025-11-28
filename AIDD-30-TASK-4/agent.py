# agent.py
from __future__ import annotations
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# If you are not sure which model is available, run the list_models snippet below.
# Default fallback model (commonly available): "gemini-2.0-flash"
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

def _read_api_key() -> str | None:
    """Look for the Gemini key in several common locations."""
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    # Streamlit secrets (UI or secrets.toml)
    try:
        import streamlit as st  # type: ignore

        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:
        pass

    # Raw .streamlit/secrets.toml file fallback when st.secrets isn't available
    secrets_path = os.path.join(".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        try:
            import tomllib  # Python 3.11+
        except ModuleNotFoundError:
            import tomli as tomllib  # type: ignore

        try:
            with open(secrets_path, "rb") as fh:
                data = tomllib.load(fh)
                key = data.get("GEMINI_API_KEY") or data.get("default", {}).get("GEMINI_API_KEY")
                if key:
                    return key
        except Exception:
            pass

    return None

_GEMINI_API_KEY = _read_api_key()
_CLIENT: genai.Client | None = None

def _get_client() -> genai.Client:
    """Create the Gemini client lazily so missing keys don't break imports."""
    global _CLIENT, _GEMINI_API_KEY

    if _CLIENT:
        return _CLIENT

    if not _GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Set it in environment variables, "
            "Streamlit secrets, or .streamlit/secrets.toml."
        )

    _CLIENT = genai.Client(api_key=_GEMINI_API_KEY, vertexai=False)
    return _CLIENT

def _extract_text_from_response(resp) -> str:
    """
    Robust parsing of various SDK response shapes.
    """
    # Common attributes in different SDK versions:
    # resp.text
    # resp.candidates[0].content / .text
    # resp.output[0].content[0].text
    try:
        if hasattr(resp, "text") and resp.text:
            return resp.text
        if hasattr(resp, "candidates") and len(resp.candidates) > 0:
            c = resp.candidates[0]
            if hasattr(c, "content"):
                return c.content
            if hasattr(c, "text"):
                return c.text
        if hasattr(resp, "output") and len(resp.output) > 0:
            # some SDKs nest content inside output -> content -> text
            out0 = resp.output[0]
            if hasattr(out0, "content") and len(out0.content) > 0:
                c0 = out0.content[0]
                if hasattr(c0, "text"):
                    return c0.text
                if hasattr(c0, "markdown"):
                    return c0.markdown
                if isinstance(c0, dict):
                    # try common keys
                    for k in ("text", "content", "markdown"):
                        if k in c0:
                            return c0[k]
        # Fallback: string representation
        return str(resp)
    except Exception:
        return str(resp)

class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        """
        Send prompt to Gemini and return plain text result.
        This function uses client.models.generate_content which is
        compatible with many SDK versions. If your SDK doesn't support
        it, run client.models.list() and adjust MODEL_NAME accordingly.
        """
        client = _get_client()

        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return _extract_text_from_response(resp)

# Optional utility: list available models (uncomment to run locally for debugging)
if __name__ == "__main__":
    try:
        models = _get_client().models.list()
        print("Available models:")
        for m in models:
            print("-", getattr(m, "name", str(m)))
    except Exception as e:
        print("List models error:", e)
