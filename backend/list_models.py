import os
import sys
from dotenv import load_dotenv

sys.path.append(r"C:\Users\sonuk\Desktop\ai boot\backend")
env_path = r"C:\Users\sonuk\Desktop\ai boot\.env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
import google.generativeai as genai

output_path = r"C:\Users\sonuk\Desktop\ai boot\models_list.txt"

with open(output_path, "w") as f:
    f.write(f"API_KEY loaded: {API_KEY[:6]}...\n")
    try:
         genai.configure(api_key=API_KEY)
         f.write("Available Models:\n")
         for m in genai.list_models():
              if 'generateContent' in m.supported_generation_methods:
                   f.write(f"- {m.name} ({m.display_name})\n")
    except Exception as e:
         f.write(f"Error listing: {str(e)}\n")

print("Finished listing. Check models_list.txt")
