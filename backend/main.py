import sys
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid
from typing import Optional, List

# Ensure relative imports work safely inside flat structure
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from endee_client import endee_client
from embedding import embedding_generator
from pdf_processor import pdf_processor
from rag_pipeline import rag_pipeline

app = FastAPI(title="AI Study Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, "..", "frontend")

app.mount("/frontend", StaticFiles(directory=frontend_dir, html=True), name="frontend")
app.mount("/static", StaticFiles(directory=frontend_dir, html=True), name="static")

class QuestionRequest(BaseModel):
    prompt: str
    sources: Optional[List[str]] = []

@app.get("/")
def home():
    return {"status": "running"}

INDEX_NAME = "study_materials"

def process_upload(content: bytes, filename: str):
    try:
        from pdf_processor import pdf_processor
        from embedding import embedding_generator
        from endee_client import endee_client
        
        if filename.endswith(".pdf"):
            text = pdf_processor.extract_text(content)
        elif filename.endswith(".txt"):
            text = content.decode("utf-8")
        else:
            return

        if not text.strip(): return

        chunks = pdf_processor.chunk_text(text)
        embeddings = embedding_generator.get_embeddings(chunks)

        points = []
        for chunk, vector in zip(chunks, embeddings):
             points.append({
                 "id": str(uuid.uuid4()),
                 "vector": vector,
                 "payload": {"text": chunk, "source": filename}
             })

        try:
             endee_client.create_index(INDEX_NAME, dimension=1536)
        except Exception:
             pass

        endee_client.insert_vectors(INDEX_NAME, points)
        print(f"Background Upload Success: {filename}")
    except Exception as e:
        print(f"Background upload error for {filename}: {e}")

@app.post("/api/v1/materials/upload")
async def upload_material(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks):
    if not file.filename.endswith((".pdf", ".txt")):
         raise HTTPException(status_code=400, detail="Only PDF and TXT files supported.")
    
    content = await file.read()
    background_tasks.add_task(process_upload, content, file.filename)
    return {"status": "success", "message": "File received. Processing started in background."}

@app.get("/api/v1/materials")
async def list_materials():
    file_path = "study_materials_db.json"
    if os.path.exists(file_path):
        import json
        try:
             with open(file_path, "r") as f:
                 points = json.load(f)
                 sources = list(set([p.get("payload", {}).get("source", "Unknown") for p in points if p.get("payload")]))
                 return {"materials": sources}
        except Exception:
             return {"materials": []}
    return {"materials": []}

@app.post("/api/v1/assistant/ask")
async def ask_question(request: QuestionRequest):
    if not request.prompt:
         raise HTTPException(status_code=400, detail="Prompt is required.")

    vectors = embedding_generator.get_embeddings([request.prompt])
    vector = vectors[0]

    try:
         search_response = endee_client.search(INDEX_NAME, vector, limit=3, sources=request.sources)
         hits = search_response.get("hits", [])
    except Exception:
         hits = []

    context_chunks = [hit.get("payload", {}).get("text", "") for hit in hits]
    context = "\n\n".join(context_chunks) if context_chunks else "No relevant context found."

    answer = rag_pipeline.generate_answer(request.prompt, context)
    return {
        "status": "success",
        "data": answer,
        "response": answer,
        "context": context[:200] + "..." if len(context) > 200 else context
    }

class QuizRequest(BaseModel):
    difficulty: str = "Medium"
    count: int = 5
    topic: str = ""

class TranslateRequest(BaseModel):
    text: str
    target_language: str

class ScoreResult(BaseModel):
    username: str
    score: int
    total: int
    difficulty: Optional[str] = "Medium"

@app.post("/api/v1/quiz/generate")
async def generate_quiz(request: QuizRequest):
    topic = request.topic.strip() if request.topic else "General Knowledge"
    
    filename = "".join([c for c in topic if c.isalnum() or c in (' ', '_', '-')]).strip().lower().replace(' ', '_') + ".json"
    file_path = os.path.join(os.path.dirname(__file__), "data", "quiz", filename)
    
    import random
    import json
    if os.path.exists(file_path):
         try:
              with open(file_path, "r", encoding="utf-8") as f:
                   questions = json.load(f)
              count = max(1, min(len(questions), request.count))
              return {"questions": random.sample(questions, count)}
         except Exception as e:
              print(f"Error reading quiz file {filename}: {e}")

    STATIC_CATEGORIES = ["Java", "Python", "C/C++", "DSA", "Web Development", "Artificial Intelligence", "Machine Learning", "Data Science", "Cyber Security", "Cloud Computing", "DBMS", "Operating System", "Networking", "General Knowledge", "Aptitude", "Logical Reasoning", "Current Affairs", "Project-Based", "Mixed"]
    
    if topic in STATIC_CATEGORIES:
         from quiz_generator import quiz_generator
         questions = quiz_generator.generate_quiz(context="", difficulty=request.difficulty, count=request.count, category=topic)
         return {"questions": questions}

    vectors = embedding_generator.get_embeddings([topic])
    vector = vectors[0]
    try:
        search_response = endee_client.search(INDEX_NAME, vector, limit=5)
        hits = search_response.get("hits", [])
    except Exception:
        hits = []

    context_chunks = [hit.get("payload", {}).get("text", "") for hit in hits]
    context = "\n\n".join(context_chunks) if context_chunks else "No relevant context found to generate quiz."

    from quiz_generator import quiz_generator
    questions = quiz_generator.generate_quiz(context, request.difficulty, request.count)
    return {"questions": questions}

@app.post("/api/v1/translate")
async def translate_text(request: TranslateRequest):
    try:
        if not request.text.strip():
             raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        prompt = f"Translate the following text into {request.target_language}. Only return the translated text.\n\nText: {request.text}"
        translated = rag_pipeline.generate_answer(prompt, context="Translate mode.")
        return {"status": "success", "translated_text": translated}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/v1/quiz/results")
async def save_score(result: ScoreResult):
    file_path = "quiz_results.json"
    results = []
    if os.path.exists(file_path):
        import json
        try:
             with open(file_path, "r") as f:
                 results = json.load(f)
        except Exception:
             results = []
    results.append(result.dict())
    try:
        with open(file_path, "w") as f:
             json.dump(results, f, indent=4)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to save score: {e}")
    return {"message": "Score saved successfully"}

@app.get("/api/v1/quiz/results")
async def get_scores():
    file_path = "quiz_results.json"
    if os.path.exists(file_path):
        import json
        try:
             with open(file_path, "r") as f:
                 return json.load(f)
        except Exception:
             return []
    return []

class DeleteRequest(BaseModel):
    filename: str

@app.post("/api/v1/materials/delete")
async def delete_material(request: DeleteRequest):
    file_path = "study_materials_db.json"
    if os.path.exists(file_path):
        import json
        try:
             with open(file_path, "r") as f:
                  points = json.load(f)
             filtered_points = [p for p in points if p.get("payload", {}).get("source") != request.filename]
             with open(file_path, "w") as f:
                  json.dump(filtered_points, f, indent=4)
             return {"message": f"Deleted {request.filename} from local index."}
        except Exception as e:
             raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Index empty or file not found."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
