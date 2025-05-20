````markdown
# 📄 Document Embedding & Vector Search Pipeline

A modular pipeline for ingesting internal PDFs (including scanned documents), extracting text, chunking content, generating vector embeddings using OpenAI, and storing them in a vector database (FAISS) for semantic search.

---

## 🚀 Features

- ✅ Supports both native and scanned PDFs  
- 🧠 OCR via OpenAI GPT-4 Vision (for scanned/image-based documents)  
- 📚 Text chunking using LangChain's `RecursiveCharacterTextSplitter`  
- 🔍 Embedding generation using OpenAI's `text-embedding-3-small`  
- 💾 Vector storage with FAISS  
- 🖥️ Streamlit front-end for quick interaction (optional)  
- 📁 Batch PDF processing supported  

---

## 📁 Project Structure

```bash
.
├── .env                        # OpenAI API keys and config variables
├── .gitignore                 
├── app.py                     # Streamlit interface (optional UI)
├── config.py                  # Central configuration
├── create_db.py               # Main pipeline to process PDFs and build FAISS DB
├── embedding_pipeline.py      # Chunking & embedding logic
├── key_checker.py             # Validates API key availability
├── pdf_processor.py           # OCR and PDF loading logic
├── ReadMe.md                  # This file
├── requirements.txt           # Python dependencies
├── utils.py                   # Helper functions
````

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file with your OpenAI API key and model config:

```
OPENAI_API_KEY=your-key-here
openai_model=gpt-4-vision-preview
embedding_model=text-embedding-3-small
chunk_size=500
chunk_overlap=50
dpi=300
pdfs_folder=./pdfs
db_path=./faiss_index
maxtokens=1000
```

---

## 📦 Usage

### ▶️ Option 1: Run the Pipeline

Process all PDFs in the configured folder and store embeddings:

```bash
python create_db.py
```

### ▶️ Option 2: Launch Streamlit App (if available)

```bash
streamlit run app.py
```

---

## 🧪 Example Flow

1. Load and OCR PDFs from `/pdfs` folder
2. Chunk extracted text into 500-token segments
3. Generate vector embeddings via OpenAI
4. Store vectors locally using FAISS
5. (Optional) Use Streamlit UI to query/search

---

## 🧰 Tech Stack

* **LangChain**
* **OpenAI API** (GPT-4 Vision + Embeddings)
* **PyMuPDF (`fitz`)**
* **FAISS**
* **Streamlit** (for UI)

---

## 📌 Notes

* OCR is only triggered if PDF is image-based or loading fails.
* Supports both programmatic and UI-driven workflows.
* Easily extendable to use cloud vector stores like Pinecone.

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

## 🙋‍♂️ Author

**Jabir**
For queries, reach out via email or GitHub issues.

```

