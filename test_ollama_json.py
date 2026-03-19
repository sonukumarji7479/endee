import httpx
import os
import json

system_prompt = (
   "You are an AI tutor. You MUST strictly respond in a valid JSON object matching this structure exactly:\n"
   "{\n"
   "  \"title\": \"Topic\",\n"
   "  \"sections\": [\n"
   "    {\"heading\": \"Definition\", \"content\": \"...\"},\n"
   "    {\"heading\": \"Features\", \"content\": \"...\"},\n"
   "    {\"heading\": \"Advantages\", \"content\": \"...\"},\n"
   "    {\"heading\": \"Use Cases\", \"content\": \"...\"},\n"
   "    {\"heading\": \"Example\", \"content\": \"...\"}\n"
   "  ]\n"
   "}\n"
   "Keep the 'content' of each section extremely concise (1-2 sentences max). Do not output anything else."
)

payload = {
    "model": "gemma:latest",
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Question: what is java"}
    ],
    "stream": False,
    "format": "json"
}

try:
    response = httpx.post("http://localhost:11434/api/chat", json=payload, timeout=120.0)
    print("STATUS CODE:", response.status_code)
    print("RESPONSE JSON:", json.dumps(response.json(), indent=2))
except Exception as e:
    print("ERROR:", str(e))
