import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

# FIXED CLIENT INITIALIZATION
client = genai.Client(
    api_key=GEMINI_API_KEY,
    api_endpoint="https://generativelanguage.googleapis.com"
)

def _extract_text_from_response(resp):
    try:
        if hasattr(resp, "text") and resp.text:
            return resp.text
        if hasattr(resp, "candidates") and resp.candidates:
            c = resp.candidates[0]
            if hasattr(c, "text"):
                return c.text
            if hasattr(c, "content"):
                return c.content
        if hasattr(resp, "output"):
            out0 = resp.output[0]
            c0 = out0.content[0]
            return getattr(c0, "text", str(resp))
        return str(resp)
    except:
        return str(resp)

class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY not set")

        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return _extract_text_from_response(resp)
