import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

class QuizGenerator:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

        # Static Fallback Questions Pool for 100% uptime guarantee on common topics
        self.static_pool = {
            "Java": [
                {"question": "What is the size of int in Java?", "options": ["2 bytes", "4 bytes", "8 bytes", "Depends on architecture"], "answer": "4 bytes"},
                {"question": "Which keyword is used to inherit a class in Java?", "options": ["implements", "inherits", "extends", "super"], "answer": "extends"},
                {"question": "What is the default value of a boolean variable in Java?", "options": ["true", "false", "null", "undefined"], "answer": "false"}
            ],
            "Python": [
                {"question": "Which of the following is an immutable data type in Python?", "options": ["List", "Dictionary", "Set", "Tuple"], "answer": "Tuple"},
                {"question": "How do you start a comment in Python?", "options": ["//", "#", "/*", "<!--"], "answer": "#"},
                {"question": "What does PEP 8 stand for?", "options": ["Python Enhancement Proposal 8", "Python Enterprise Package 8", "Primary Execution Phase 8", "None of the above"], "answer": "Python Enhancement Proposal 8"}
            ]
        }

    def generate_quiz(self, context: str = "", difficulty: str = "Medium", count: int = 5, category: str = None) -> list:
        # 1. Try to serve from Static Pool first if category matches and count is small enough
        if category and category in self.static_pool and count <= len(self.static_pool[category]):
             return self.static_pool[category][:count]

        target_topic = category if category else "General Knowledge"
        if context:
             target_topic = f"the following text:\n\n{context[:2000]}"

        prompt = f"""
Generate {count} multiple choice questions with {difficulty} difficulty based on {target_topic}.
The output MUST be a valid JSON array. DO NOT include markdown code blocks like ```json or any explanation. ONLY return the raw valid JSON array.

Each object in the array MUST have the exact following keys:
- "question": string
- "options": list of strings (provide 4 options)
- "answer": string (must match EXACTLY one of the strings in the "options" list)

Example Output Format:
[
  {{
    "question": "What does AI stand for?",
    "options": ["Artificial Intelligence", "Automated Interface", "Active Integration", "All In"],
    "answer": "Artificial Intelligence"
  }}
]
"""

        if self.provider != "ollama" and (not self.api_key or self.api_key in ["your_openai_api_key_here", "your_gemini_api_key_here"]):
             print(f"[WARNING] API Key for {self.provider} not set for Quiz Generation. Using MOCK fallback.")
             return self._get_mock_questions(count)

        if self.provider == "gemini":
             try:
                  import google.generativeai as genai
                  genai.configure(api_key=self.api_key)
                  model = genai.GenerativeModel('gemini-1.5-flash')
                  response = model.generate_content(prompt)
                  return self._parse_and_clean_json(response.text, count)
             except Exception as e:
                  print(f"Gemini Quiz Gen Error: {e}")
                  return self._get_mock_questions(count)

        # Ollama Fallback
        elif self.provider == "ollama":
             try:
                  import httpx
                  payload = {
                       "model": os.getenv("OLLAMA_MODEL", "gemma"),
                       "messages": [{"role": "user", "content": prompt}],
                       "stream": False
                  }
                  response = httpx.post(f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/chat", json=payload, timeout=60.0)
                  text = response.json()["message"]["content"]
                  return self._parse_and_clean_json(text, count)
             except Exception as e:
                  print(f"Ollama Quiz Gen Error: {e}")
                  return self._get_mock_questions(count)

        return self._get_mock_questions(count)

    def _parse_and_clean_json(self, text: str, count: int) -> list:
         cleaned = text.strip()
         if cleaned.startswith("```"):
              cleaned = "\n".join(cleaned.split("\n")[1:-1]).strip()
         try:
              data = json.loads(cleaned)
              if isinstance(data, list):
                   return data[:count]
         except Exception:
              pass
         return self._get_mock_questions(count)

    def _get_mock_questions(self, count: int) -> list:
         return [
              {"question": f"Mock Question {i+1} regarding study material?", "options": ["Option A", "Option B", "Option C", "Option D"], "answer": "Option A"}
              for i in range(count)
         ]

quiz_generator = QuizGenerator()
