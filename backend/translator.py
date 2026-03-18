import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

class Translator:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

    def translate(self, text: str, target_language: str) -> str:
        system_prompt = (
            "You are a professional translator. Translate the provided text to the requested Target Language.\n"
            "Return ONLY the translated text. Do not include any notes, explanations, or greeting."
        )
        
        user_prompt = f"Text to translate:\n{text}\n\nTarget Language: {target_language}"

        if not self.api_key and self.provider != "ollama":
             return f"[MOCK TRANSLATION to {target_language}] {text}"

        if self.provider == "gemini":
             return self._translate_gemini(system_prompt, user_prompt)
        elif self.provider == "ollama":
             return self._translate_ollama(system_prompt, user_prompt)
        else:
             return self._translate_openai(system_prompt, user_prompt)

    def _translate_gemini(self, system, user):
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{system}\n\n{user}")
            return response.text
        except Exception as e:
            return f"[Gemini Translation Error] {e}"

    def _translate_ollama(self, system, user):
        try:
            import httpx
            payload = {
                "model": os.getenv("OLLAMA_MODEL", "gemma"),
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                "stream": False
            }
            response = httpx.post(
                f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/chat",
                json=payload,
                timeout=60.0
            )
            return response.json()["message"]["content"]
        except Exception as e:
            return f"[Ollama Translation Error] {e}"

    def _translate_openai(self, system, user):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
             return f"[OpenAI Translation Error] {e}"

translator = Translator()
