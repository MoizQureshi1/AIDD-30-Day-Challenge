import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

# NEW SDK INITIALIZATION
genai.configure(api_key=GEMINI_API_KEY)

# Create model instance
model = genai.GenerativeModel(MODEL_NAME)


def _extract_text_from_response(resp):
    """
    Gemini new SDK returns:
    resp.text
    resp.candidates[0].content.parts[x].text
    """
    try:
        if hasattr(resp, "text") and resp.text:
            return resp.text

        if hasattr(resp, "candidates"):
            c = resp.candidates[0]
            if hasattr(c, "content") and hasattr(c.content.parts[0], "text"):
                return c.content.parts[0].text

        return str(resp)
    except:
        return str(resp)


class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY missing")

        resp = model.generate_content(prompt)
        return _extract_text_from_response(resp)
