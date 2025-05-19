import base64
import fitz
from io import BytesIO
from PIL import Image
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import config
import openai

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

def page_to_base64_image(pdf_path, page_index):
    doc = fitz.open(pdf_path)
    page = doc[page_index]
    pix = page.get_pixmap(dpi=config.dpi)
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode('utf-8')

def ocr_pdf_with_openai(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for i in range(len(doc)):
        print(f"OCR on page {i+1}/{len(doc)}...")
        img_base64 = page_to_base64_image(pdf_path, i)
        response = openai.chat.completions.create(
            model=config.openai_model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract plain text from this scanned page."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                ]}
            ],
            max_tokens=config.maxtokens,
        )
        page_text = response.choices[0].message.content
        all_text += page_text + "\n"
    return all_text

def extract_text_from_pdf(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        if docs:
            print(f"Extracted using Langchain: {pdf_path}")
            return " ".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"Langchain loader failed: {e}")
    
    print(f"Falling back to OpenAI Vision OCR for: {pdf_path}")
    return ocr_pdf_with_openai(pdf_path)

def chunk_text(text, chunk_size=config.chunk_size,chunk_overlap=config.chunk_overlap):  
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.create_documents([text])

def store_documents_in_faiss(docs, embedding_model, db_path=config.db_path):
    db = FAISS.from_documents(docs, embedding_model)
    db.save_local(db_path)
    print(f"Vector store saved at: {db_path}")
    return db

def process_pdf_folder(folder_path):
    all_chunks = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            print(f"Processing: {file}")
            text = extract_text_from_pdf(full_path)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    folder = config.pdfs_folder
    documents = process_pdf_folder(folder)
    print("Generating embeddings...")
    embeddings = OpenAIEmbeddings(model=config.embedding_model)
    store_documents_in_faiss(documents, embeddings)
