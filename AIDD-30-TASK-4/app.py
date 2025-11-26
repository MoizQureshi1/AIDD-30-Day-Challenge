# app.py
import streamlit as st
import os
from pdf_utils import extract_pdf_text
from agent import Agent

st.set_page_config(page_title="PDF Summarizer & Quiz Generator", layout="wide")
st.title("📘 PDF Summarizer & Quiz Generator")

# session state
for k in ("pdf_path", "summary", "quiz"):
    if k not in st.session_state:
        st.session_state[k] = ""

uploaded = st.file_uploader("Upload PDF", type=["pdf"])
if uploaded:
    os.makedirs("data", exist_ok=True)
    pdf_path = os.path.join("data", uploaded.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())
    st.session_state.pdf_path = pdf_path
    st.success(f"Saved {uploaded.name}")

if st.session_state.pdf_path:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                txt = extract_pdf_text(st.session_state.pdf_path)
                prompt = f"Summarize the following text in 6-8 bullet points:\n\n{txt}"
                st.session_state.summary = Agent.run(prompt)
    with col2:
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                prompt = (
                    "You are an assistant. Read the PDF at this path and generate 8 MCQs with 4 options each; "
                    "mark the correct answer for each. Use a numbered list.\n"
                    f"PDF_PATH: {st.session_state.pdf_path}"
                )
                try:
                    st.session_state.quiz = Agent.run(prompt)
                except Exception as e:
                    st.error(f"Generation error: {e}")

if st.session_state.summary:
    st.subheader("📝 Summary")
    st.markdown(st.session_state.summary)

if st.session_state.quiz:
    st.subheader("❓ Quiz")
    st.markdown(st.session_state.quiz)
