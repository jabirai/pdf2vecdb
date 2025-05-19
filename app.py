import streamlit as st
from pdf_processor import extract_text
from embedding_pipeline import chunk_text, save_to_faiss
from utils import init_session, add_uploaded_files
import openai

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(layout="wide")
st.title("PDF Ingestor + FAISS Vector Store")
st.sidebar.header("Uploaded PDFs")

init_session()

uploaded = st.file_uploader("Upload one or more PDFs", type=["pdf"], accept_multiple_files=True)
if uploaded:
    add_uploaded_files(uploaded)

if st.button("Save to Vector DB"):
    if not st.session_state.uploaded_files:
        st.warning("Please upload at least one PDF first.")
    else:
        all_chunks = []
        for name, file in st.session_state.uploaded_files.items():
            st.write(f"Processing: {name}")
            text = extract_text(file, name)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
        with st.spinner("Generating embeddings and saving to FAISS..."):
            save_to_faiss(all_chunks)