from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import streamlit as st

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.create_documents([text])

def save_to_faiss(documents, db_path="faiss_index"):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(db_path)
    st.success(f"✅ Saved to vector DB at '{db_path}'")