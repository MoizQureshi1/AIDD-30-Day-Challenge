# agent.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# If you are not sure which model is available, run the list_models snippet below.
# Default fallback model (commonly available): "gemini-2.0-flash"
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

# IMPORTANT: Force API-key mode to avoid Vertex AI project requirements in many deploy envs
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env or environment before running.."
    )

client = genai.Client(api_key=GEMINI_API_KEY, vertexai=False)

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
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not set in environment (.env)")

        # Send request
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return _extract_text_from_response(resp)

# Optional utility: list available models (uncomment to run locally for debugging)
if __name__ == "__main__":
    try:
        models = client.models.list()
        print("Available models:")
        for m in models:
            print("-", getattr(m, "name", str(m)))
    except Exception as e:
        print("List models error:", e)
