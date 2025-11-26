# agent.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-2.0-flash"  # <-- Use the exact name from list_models

client = genai.Client(api_key=GEMINI_API_KEY)

class Agent:
    @staticmethod
    def run(prompt: str) -> str:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        # SDK response might return a list in .candidates[0].content
        if hasattr(response, "candidates") and len(response.candidates) > 0:
            return response.candidates[0].content
        return str(response)
