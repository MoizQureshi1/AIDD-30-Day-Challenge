# PDF Summarizer & Quiz Generator (Streamlit + Gemini)

A small Streamlit app that extracts text from uploaded PDFs, sends the text to Google Gemini (GenAI Python SDK), and returns a summary and a quiz.

## Files
- `app.py` - Streamlit application (UI + orchestration)
- `agent.py` - Gemini client wrapper (robust parsing + API-key mode)
- `pdf_utils.py` - PDF text extraction utility
- `gemini.md` - Development / role instructions
- `.env.example` - environment variables template
- `requirements.txt` - Python dependencies

## Prerequisites
- Python 3.10+ (3.11 or 3.13 recommended)
- Virtual environment (venv)

## Setup
1. Create and activate virtual env:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows PowerShell
