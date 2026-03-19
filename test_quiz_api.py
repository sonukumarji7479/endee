import httpx
import json

payload = {
    "difficulty": "Medium",
    "count": 5,
    "topic": "Java"
}

try:
    response = httpx.post("http://localhost:8000/api/v1/quiz/generate", json=payload, timeout=10.0)
    print("STATUS CODE:", response.status_code)
    print("RESPONSE JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("ERROR:", str(e))
