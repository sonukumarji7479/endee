import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    print("Listing Models:")
    for m in genai.list_models():
         print(f"Name: {m.name}, Methods: {m.supported_generation_methods}")
except Exception as e:
    print(f"Exception: {e}")
