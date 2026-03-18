import os
import sys
import json
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

class QuizGenerator:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

    def generate_quiz(self, context: str, difficulty: str = "Medium", count: int = 5, category: str = "") -> list:
        system_prompt = (
            "You are an expert quiz master. Generate a Multiple Choice Question (MCQ) quiz based strictly on the provided Context or Category.\n"
            "Return ONLY valid JSON array containing objects corresponding to schema. Do not output markdown code blocks (no ````json).\n"
            "The JSON must be a list of question objects:\n"
            "[\n"
            "  {\n"
            "    \"question\": \"Question text?\",\n"
            "    \"options\": [\"Option A text\", \"Option B text\", \"Option C text\", \"Option D text\"],\n"
            "    \"answer\": \"Exact text matching one of the options above\",\n"
            "    \"explanation\": \"Brief explanation of the answer\"\n"
            "  }\n"
            "]"
        )
        
        if category and not context:
             user_prompt = f"Category: {category}\nDifficulty: {difficulty}\nGenerate {count} highly accurate questions based on this topic. Include conceptual, technical, and code-based examples if applicable."
        else:
             user_prompt = f"Context:\n{context}\n\nDifficulty: {difficulty}\nGenerate {count} questions."

        # Static Pool Check for absolute 100% stability
        if category and not context:
             db_path = os.path.join(os.path.dirname(__file__), "quiz_database.json")
             if os.path.exists(db_path):
                  try:
                       with open(db_path, "r") as f:
                            db = json.load(f)
                            if category in db and db[category]:
                                 import random
                                 questions = db[category]
                                 random.shuffle(questions)
                                 return questions[:min(count, len(questions))]
                  except Exception:
                       pass

        if not self.api_key and self.provider != "ollama":
             return self._get_mock_quiz()

        if self.provider == "gemini":
             return self._generate_gemini(system_prompt, user_prompt)
        elif self.provider == "ollama":
             return self._generate_ollama(system_prompt, user_prompt)
        else:
             return self._generate_openai(system_prompt, user_prompt)

    def _generate_gemini(self, system, user):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-2.5-flash") # Ideal for fast generation
            
            response = model.generate_content(
                f"{system}\n\n{user}",
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[QuizGenerator] Gemini Error: {e}")
            return self._get_mock_quiz()

    def _generate_ollama(self, system, user):
        try:
            import httpx
            payload = {
                "model": os.getenv("OLLAMA_MODEL", "gemma"),
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "stream": False,
                "format": "json"
            }
            response = httpx.post(
                f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/chat",
                json=payload,
                timeout=60.0
            )
            text = response.json()["message"]["content"]
            return json.loads(text)
        except Exception as e:
            print(f"[QuizGenerator] Ollama Error: {e}")
            return self._get_mock_quiz()

    def _generate_openai(self, system, user):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            text = response.choices[0].message.content
            # OpenAI response_format json_object requires prompt to mention "json"
            # It returns a dict, so if it's `{ "questions": [...] }` we need list
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "questions" in parsed:
                return parsed["questions"]
            return parsed
        except Exception as e:
             print(f"[QuizGenerator] OpenAI Error: {e}")
             return self._get_mock_quiz()

    def _get_mock_quiz(self):
        return [
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "London", "Paris", "Madrid"],
                "answer": "Paris",
                "explanation": "Paris is the capital and largest city of France."
            },
             {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Jupiter", "Mars", "Venus"],
                "answer": "Mars",
                "explanation": "Mars has iron oxide on its surface giving it a reddish appearance."
            }
        ]

quiz_generator = QuizGenerator()
