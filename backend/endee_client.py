import httpx
import os
from dotenv import load_dotenv

load_dotenv()

class EndeeClient:
    def __init__(self):
        self.base_url = os.getenv("ENDEE_API_URL", "http://localhost:8080")
        self.auth_token = os.getenv("ENDEE_AUTH_TOKEN", "")
        self.headers = {"Content-Type": "application/json"}
        if self.auth_token:
            self.headers["Authorization"] = self.auth_token

    def check_health(self):
        try:
             with httpx.Client() as client:
                  response = client.get(f"{self.base_url}/api/v1/health", headers=self.headers)
                  return response.json()
        except Exception as e:
             return {"status": "error", "message": str(e)}

    def insert_vectors(self, index_name: str, points: list):
        try:
             with httpx.Client() as client:
                  payload = {"points": points}
                  response = client.post(f"{self.base_url}/api/v1/index/{index_name}/insert", json=payload, headers=self.headers)
                  return response.json()
        except Exception as e:
             print(f"[FALLBACK] Endee DB insert failed ({str(e)}). Storing offline in {index_name}_db.json")
             self._save_to_local_store(index_name, points)
             return {"status": "fallback", "message": "Saved to local JSON store"}

    def search(self, index_name: str, vector: list, limit: int = 5, sources: list = None):
        try:
             with httpx.Client() as client:
                  payload = {"vector": vector, "limit": limit}
                  if sources:
                       payload["sources"] = sources
                  response = client.post(f"{self.base_url}/api/v1/index/{index_name}/search", json=payload, headers=self.headers)
                  return response.json()
        except Exception as e:
             print(f"[FALLBACK] Endee DB search failed ({str(e)}). Calculating from local storage.")
             return self._search_local_store(index_name, vector, limit, sources)

    def _save_to_local_store(self, index_name: str, points: list):
         import json
         filename = f"{index_name}_db.json"
         try:
              with open(filename, 'r') as f:
                   existing = json.load(f)
         except Exception:
              existing = []
         existing.extend(points)
         with open(filename, 'w') as f:
              json.dump(existing, f)

    def _search_local_store(self, index_name: str, vector: list, limit: int = 5, sources: list = None):
         import json
         filename = f"{index_name}_db.json"
         try:
              with open(filename, 'r') as f:
                   points = json.load(f)
         except Exception:
              return {"hits": []}

         def cosine_similarity(v1, v2):
              dot = sum(a*b for a, b in zip(v1, v2))
              norm1 = sum(a*a for a in v1) ** 0.5
              norm2 = sum(b*b for b in v2) ** 0.5
              return dot / (norm1 * norm2) if (norm1 > 0 and norm2 > 0) else 0

         scored_points = []
         for p in points:
              p_vector = p.get("vector")
              if p_vector:
                   p_source = p.get("payload", {}).get("source")
                   if sources and p_source not in sources:
                        continue

                   score = cosine_similarity(vector, p_vector)
                   # Endee format lists payload: {}
                   scored_points.append({"score": score, "payload": p.get("payload", {})})

         scored_points.sort(key=lambda x: x["score"], reverse=True)
         return {"hits": scored_points[:limit]}

endee_client = EndeeClient()
