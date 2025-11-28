import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")

# NEW SDK
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def _extract_text_from_response(resp):
    try:
        if resp.text:
            return resp.text
        if resp.candidates:
            return resp.candidates[0].content.parts[0].text
        return str(resp)
    except:
        return str(resp)

class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        resp = model.generate_content(prompt)
        return _extract_text_from_response(resp)
