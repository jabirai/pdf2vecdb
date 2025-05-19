import openai
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

def check_openai_key():
    try:
        # Simple test: list models
        models = openai.models.list()
        print("API key is valid. Available models:")
        for model in models.data[:5]:  # just show top 5
            print("-", model.id)
    except openai.error.AuthenticationError:
        print("Invalid OpenAI API key.")
    except Exception as e:
        print("Error:", e)

check_openai_key()
