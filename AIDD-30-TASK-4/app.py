# app.py
import os
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import extract_pdf_text
from agent import Agent

load_dotenv()

st.set_page_config(page_title="PDF Summarizer & Quiz Generator", layout="wide")
st.title("📘 PDF Summarizer & Quiz Generator")

# ensure data folder exists
os.makedirs("data", exist_ok=True)

# session state defaults
for k in ("pdf_path", "summary", "quiz"):
    if k not in st.session_state:
        st.session_state[k] = ""

# Upload UI
uploaded = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded:
    pdf_path = os.path.join("data", uploaded.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())
    st.session_state.pdf_path = pdf_path
    st.success(f"Saved {uploaded.name}")

# Buttons & generation
if st.session_state.pdf_path:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Summary"):
            with st.spinner("Extracting text and generating summary..."):
                try:
                    txt = extract_pdf_text(st.session_state.pdf_path)
                    if not txt.strip():
                        st.error("Could not extract text from PDF (maybe scanned/ image PDF).")
                    else:
                        prompt = (
                            "You are an expert summarizer. Read the following document text and produce a "
                            "concise structured summary in 6-8 bullet points. Keep bullets short and clear.\n\n"
                            f"{txt}\n\nSummary:"
                        )
                        st.session_state.summary = Agent.run(prompt)
                except Exception as e:
                    st.error(f"Generation error: {e}")

    with col2:
        if st.button("Generate Quiz"):
            with st.spinner("Extracting text and generating quiz..."):
                try:
                    txt = extract_pdf_text(st.session_state.pdf_path)
                    if not txt.strip():
                        st.error("Could not extract text from PDF (maybe scanned/ image PDF).")
                    else:
                        prompt = (
                            "You are a quiz generator. From the text below, create 8 multiple-choice questions (MCQs). "
                            "Each question should have 4 options labeled A–D, and indicate the correct option. "
                            "Keep questions short and clearly tied to the text.\n\n"
                            f"{txt}\n\nQuiz:"
                        )
                        st.session_state.quiz = Agent.run(prompt)
                except Exception as e:
                    st.error(f"Generation error: {e}")

# Display results
if st.session_state.summary:
    st.subheader("📝 Summary")
    st.markdown(st.session_state.summary)

if st.session_state.quiz:
    st.subheader("❓ Quiz")
    st.markdown(st.session_state.quiz)
