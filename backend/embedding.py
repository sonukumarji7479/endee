import openai
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("OPENAI_API_KEY") if self.provider == "openai" else os.getenv("GEMINI_API_KEY")
        if self.provider == "gemini" and self.api_key and self.api_key != "your_gemini_api_key_here":
             import google.generativeai as genai
             genai.configure(api_key=self.api_key)

    def get_embeddings(self, texts: list) -> list:
        if not self.api_key or self.api_key in ["your_openai_api_key_here", "your_gemini_api_key_here"]:
              print(f"[WARNING] API Key for {self.provider} not set. Using Random MOCK Embeddings.")
              import random
              return [[random.uniform(-1, 1) for _ in range(1536)] for _ in texts]

        if self.provider == "gemini":
             try:
                  import google.generativeai as genai
                  embeddings = []
                  for text in texts:
                       result = genai.embed_content(
                            model="models/text-embedding-004",
                            content=text,
                            task_type="retrieval_document"
                       )
                       vec = result['embedding']
                       if len(vec) < 1536:
                            vec = vec + [0.0] * (1536 - len(vec))
                       embeddings.append(vec)
                  return embeddings
             except Exception as e:
                  print(f"Gemini Embedding Error: {e}")
                  import random; return [[random.uniform(-1, 1) for _ in range(1536)] for _ in texts]

        elif self.provider == "ollama":
             try:
                  import httpx
                  embeddings = []
                  model_name = os.getenv("OLLAMA_MODEL", "gemma")
                  host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
                  for text in texts:
                       res = httpx.post(f"{host}/api/embeddings", json={"model": model_name, "prompt": text}, timeout=60.0)
                       vec = res.json()["embedding"]
                       if len(vec) < 1536:
                            vec = vec + [0.0] * (1536 - len(vec))
                       embeddings.append(vec[:1536])
                  return embeddings
             except Exception as e:
                  print(f"Ollama Embedding Error: {e}")
                  import random; return [[random.uniform(-1, 1) for _ in range(1536)] for _ in texts]

        try:
              from openai import OpenAI
              client = OpenAI(api_key=self.api_key)
              response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
              return [data.embedding for data in response.data]
        except Exception:
              import random
              return [[random.uniform(-1, 1) for _ in range(1536)] for _ in texts]

embedding_generator = EmbeddingGenerator()
