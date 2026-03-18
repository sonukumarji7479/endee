import os
import json
import sys
from dotenv import load_dotenv

sys.path.append(r"C:\Users\sonuk\Desktop\ai boot\backend")
env_path = r"C:\Users\sonuk\Desktop\ai boot\.env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
import google.generativeai as genai

output_path = r"C:\Users\sonuk\Desktop\ai boot\debug_seeder.txt"

with open(output_path, "w") as f:
    f.write(f"API_KEY loaded: {API_KEY[:6]}...\n")
    try:
         genai.configure(api_key=API_KEY)
         model = genai.GenerativeModel("gemini-1.5-flash")
         
         prompt = """You are an expert quiz master. Generate 10 distinct Multiple Choice Questions for the category: Java.
         Return ONLY valid JSON array with exact schema:
         [
           {
             "question": "Question text?",
             "options": ["Option A", "Option B", "Option C", "Option D"],
             "answer": "Exact options text matching the correct answer",
             "explanation": "Brief explanation"
           }
         ]"""
         
         response = model.generate_content(
             prompt,
             generation_config={"response_mime_type": "application/json"}
         )
         f.write(f"Response status: SUCCESS\n")
         f.write(f"Response text: {response.text}\n")
    except Exception as e:
         f.write(f"Error occurred: {str(e)}\n")

print("Debug Finished. Written to debug_seeder.txt")
