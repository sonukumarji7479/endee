import os
import sys
from dotenv import load_dotenv

load_dotenv()

class Translator:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

    def translate(self, text: str, target_language: str) -> str:
        prompt = f"Translate the following text strictly into {target_language}. Return ONLY the translated text, no explanation or markdown code blocks:\n\n{text}"

        if not self.api_key or self.api_key in ["your_openai_api_key_here", "your_gemini_api_key_here"]:
             print(f"[WARNING] API Key for {self.provider} not set for Translation. Using MOCK fallback.")
             return f"[MOCK TRANSLATION to {target_language}] {text}"

        if self.provider == "gemini":
             try:
                  import google.generativeai as genai
                  genai.configure(api_key=self.api_key)
                  model = genai.GenerativeModel('gemini-1.5-flash')
                  response = model.generate_content(prompt)
                  return response.text.strip()
             except Exception as e:
                  print(f"Gemini Translate Error: {e}")
                  return f"Translation Error: {e}"

        elif self.provider == "ollama":
             try:
                  import httpx
                  payload = {
                       "model": os.getenv("OLLAMA_MODEL", "gemma"),
                       "messages": [{"role": "user", "content": prompt}],
                       "stream": False
                  }
                  response = httpx.post(f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/chat", json=payload, timeout=60.0)
                  return response.json()["message"]["content"].strip()
             except Exception as e:
                  print(f"Ollama Translate Error: {e}")
                  return f"Translation Error: {e}"

        return f"[MOCK] {text}"

translator = Translator()
