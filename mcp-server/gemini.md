# Role: Senior Python AI Engineer

Objective: Build a **PDF Summarizer & Quiz Generator Agent** using:
- Streamlit UI
- OpenAgents SDK
- PyPDF for PDF text extraction
- Gemini LLM
- Context7 MCP server

## Restrictions (MUST FOLLOW)
1. No extra code. Only core logic.
2. Use ONLY OpenAgents SDK syntax.
3. Avoid hallucinated features.
4. Use PyPDF ONLY for reading PDF.
5. All logic inside 3 main files: tools.py, agent.py, app.py.
6. Agent must generate:
   - PDF Summary
   - Quiz from original PDF

## Architecture
.
├── pdf_utils.py      # PDF extraction tools
├── tools.py          # Agent tools for summarization & quiz
├── agent.py          # Gemini + Tools bindings
├── app.py            # Streamlit UI
└── .env              # API Key

## Agent Capabilities
- Accept PDF upload
- Extract text using PyPDF
- Summarize text using Gemini
- Create quiz (MCQs or mixed)
- Display results in Streamlit UI

