import httpx
import os

url = "http://localhost:8000/api/v1/materials/upload"
file_path = "java_study_guide.txt"

if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("This is a test study guide about Java.")

try:
    with open(file_path, 'rb') as f:
        files = {'file': f}
        res = httpx.post(url, files=files, timeout=60.0)
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}")
except Exception as e:
    print(f"Error: {e}")
