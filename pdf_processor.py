import fitz
import base64
from langchain.document_loaders import PyPDFLoader
import openai
import config
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text(file_bytes, file_name):
    try:
        with open(f"./tempfiles/temp_{file_name}", "wb") as f:
            f.write(file_bytes.read())
        loader = PyPDFLoader(f"./tempfiles/temp_{file_name}")
        docs = loader.load()
        if docs:
            return " ".join([doc.page_content for doc in docs])
    except:
        pass
    return ocr_with_gpt4vision(file_bytes)

def pdf_bytes_to_images(file_bytes):
    pdf_doc = fitz.open("pdf", file_bytes.getvalue())
    images = []
    for page in pdf_doc:
        pix = page.get_pixmap(dpi=config.dpi)
        img_bytes = pix.tobytes("png")
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        images.append(img_base64)
    return images

def ocr_with_gpt4vision(file_bytes):
    all_text = ""
    images = pdf_bytes_to_images(file_bytes)
    for idx, img in enumerate(images):
        response = openai.chat.completions.create(
            model=config.openai_model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": "Extract text from this document page."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}
                ]}
            ],
            max_tokens=config.maxtokens,
        )
        text = response.choices[0].message.content
        all_text += text + "\n"
    return all_text