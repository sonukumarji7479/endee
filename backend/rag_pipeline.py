import openai
import os
import sys
from dotenv import load_dotenv

# Ensure local imports work regardless of CWD
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from endee_client import endee_client
from embedding import embedding_generator

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.index_name = "study_materials"
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")

    def _generate_gemini(self, prompt: str, context: str) -> str:
        try:
             import google.generativeai as genai
             api_key = os.getenv("GEMINI_API_KEY")
             if not api_key or api_key == "your_gemini_api_key_here":
                  return "Gemini Error: API Key is missing or placeholder."
             genai.configure(api_key=api_key)
             
             if not hasattr(self, 'available_gemini_models'):
                  try: self.available_gemini_models = [m.name.split('/')[-1] for m in genai.list_models()]
                  except Exception: self.available_gemini_models = ['gemini-1.5-flash']

             candidates = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-1.5-pro']
             test_models = [c for c in candidates if c in self.available_gemini_models] or ['gemini-1.5-flash']

             last_error = ""
             for model_name in test_models:
                  try:
                       model = genai.GenerativeModel(model_name)
                       system_prompt = "You are an engaging and helpful study assistant. Answer questions clearly using the context provided."
                       full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nQuestion:\n{prompt}"
                       response = model.generate_content(full_prompt)
                       return response.text
                  except Exception as e:
                       last_error = str(e)
                       if "429" in last_error or "quota" in last_error.lower(): continue
                       return f"Gemini Error on {model_name}: {last_error}"
             return f"Gemini Error: All candidates failed. Last error: {last_error}"
        except Exception as e:
             return f"Gemini setup error: {str(e)}"

    def generate_answer(self, prompt: str, context: str) -> str:
        if self.provider != "ollama" and (not self.api_key or self.api_key in ["your_openai_api_key_here", "your_gemini_api_key_here"]):
             return f"[MOCK ANSWER based on Context] Context excerpt: {context[:100]}... Question: {prompt}"

        if self.provider == "gemini":
             return self._generate_gemini(prompt, context)

        elif self.provider == "ollama":
             try:
                  import httpx
                  import json
                  system_prompt = (
                       "You are a powerful AI tutor. Answer any question in a structured format using EXACTLY these headings with emojis:\n"
                       "📌 Definition\n"
                       "⚡ Key Points\n"
                       "🚀 Advantages\n"
                       "💡 Example\n\n"
                       "Keep answers extremely concise and clear."
                  )
                  payload = {
                      "model": os.getenv("OLLAMA_MODEL", "gemma"),
                      "prompt": f"{system_prompt}\n\nContext: {context}\n\nQuestion: {prompt}",
                      "stream": False
                  }
                  response = httpx.post(f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/generate", json=payload, timeout=120.0)
                  res_json = response.json()
                  if "response" in res_json:
                      return res_json["response"]
                  
                  # Resilient Fallback to Gemini on local RAM exhaustion
                  error_msg = str(res_json.get("error", "")).lower()
                  if "memory" in error_msg or "available" in error_msg:
                      return self._generate_gemini(prompt, context)

                  return f"Ollama Error Structure: {json.dumps(res_json)}"
             except Exception as e:
                  if "memory" in str(e).lower():
                      return self._generate_gemini(prompt, context)
                  return f"Ollama Error: {str(e)}"

        try:
             from openai import OpenAI
             client = OpenAI(api_key=self.api_key)
             system_prompt = "You are an engaging and helpful study assistant. Use the provided context to answer questions clearly, conversationally, and naturally."
             response = client.chat.completions.create(
                 model="gpt-3.5-turbo",
                 messages=[
                     {"role": "system", "content": system_prompt},
                     {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
                 ]
             )
             return response.choices[0].message.content
        except Exception:
             return "Error generating response from LLM."

rag_pipeline = RAGPipeline()
