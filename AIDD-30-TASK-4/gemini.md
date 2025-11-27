# Role: Senior Python AI Engineer

**Objective:** Build a PDF Summarizer & Quiz Generator Agent using Streamlit + Gemini (GenAI SDK).

## Project Overview
- UI: Streamlit
- Model: Google Gemini (GenAI Python SDK) using API-key mode (vertexai=False)
- Local PDF extraction: PyPDF2
- Files: agent.py, pdf_utils.py, app.py

## Constraints
1. Use API-key mode (no Vertex project requirement).
2. Extract PDF text locally and send text to the model (do not rely on model to open local files).
3. Keep code minimal and focused on core features: summary + quiz.
4. Document exact dependencies and run commands.

## System Prompt (Agent behavior)
You are an assistant that:
- Produces clear summaries.
- Generates MCQs from provided text.
- Keeps answers concise and actionable.
