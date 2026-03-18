import os
import json
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: Loaded API_KEY={API_KEY[:6]}..." if API_KEY else "DEBUG: API_KEY NOT FOUND!")
CATEGORIES = ["Java", "Python", "C/C++", "DSA", "Web Development", "Artificial Intelligence", "Machine Learning", "Data Science", "Cyber Security", "Cloud Computing", "DBMS", "Operating System", "Networking", "General Knowledge", "Aptitude", "Logical Reasoning", "Current Affairs", "Project-Based", "Mixed"]

db = {}

def generate_for_cat(cat):
    # Standard fast HTTP request directly to avoid GenAI framework version weights in seeder.
    import google.generativeai as genai
    print(f"Seeding category: {cat}")
    prompt = f"""You are an expert quiz master. Generate 10 distinct Multiple Choice Questions for the category: {cat}.
    Provide 4 options (A, B, C, D) inside a list, a single item matching the correct answer text, and a brief explanation explaining the logic.
    Return ONLY JSON array with layout:
    [
      {{
        "question": "Question text?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Exact options text matching the correct answer",
        "explanation": "Brief explanation describing the answer"
      }}
    ]
    Do not add markdown wrapper (no ```json). Output starts with [ and ends with ]."""

    try:
         genai.configure(api_key=API_KEY)
         model = genai.GenerativeModel("gemini-2.5-flash")
         response = model.generate_content(
             prompt,
             generation_config={"response_mime_type": "application/json"}
         )
         if response.text:
              return json.loads(response.text)
    except Exception as e:
         print(f"Exception {cat}: {e}")
    return []

for cat in CATEGORIES:
    questions = generate_for_cat(cat)
    if questions:
         db[cat] = questions

with open("backend/quiz_database.json", "w") as f:
    json.dump(db, f, indent=4)
print("\nFinished seeding fallback database with", sum(len(v) for v in db.values()), "items across", len(db.keys()), "categories.")
