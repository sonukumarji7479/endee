# AI Study Assistant

A Complete AI-powered Study Assistant Web Application using **RAG (Retrieval Augmented Generation)**, built strictly with **Google Gemini / Ollama** and the **Endee Vector Database** for fast semantic search and context retrieval.

---

## 🚀 Overview

The **AI Study Assistant** allows users to upload long-form PDF materials, manage document context grids, and interact via smart **Voice AI** or Chat. It also contains a full **Quiz Engine** with fallback stability ensuring unlimited quiz generation support offline safely.

---

## 🛠 Features

- **📂 Document Management System**: 
  - Drag & Drop PDF upload and automated indexing.
  - Multi-select Document grids allowing **Filtered RAG Queries** (target specific files exclusively).
  - Delete endpoints wiping materials from queries seamlessly.
- **🎤 Complete Voice AI System**:
  - **Speech-To-Text (STT)**: Dictate inputs through mic panel bindings.
  - **Text-To-Speech (TTS)**: Let the Assistant read response bubbles aloud natively.
  - **Multi-Language Support**: Synced topbar dropdown supports **English, Hindi, Bengali, and Tamil** audio streams natively.
- **🧠 Advanced Quiz Engine**:
  - Generate MCQs based on specific Categories & Difficulties.
  - **100% Uptime Static Fallback**: Over 150+ cached questions per static static category pool ensures zero LLM timeout failures natively on requests.
- **🌐 In-App Translator**: Translate prompt answers into targeted language nodes flawlessly inside prompt views.

---

## ⚙ Tech Stack

- **Backend**: Python 3.10+ (FastAPI)
- **Frontend**: Vanilla HTML / CSS / JavaScript (Glassmorphic Styles)
- **Vector DB**: Endee Vector Database 
- **LLM / Embedding Models**: Google Gemini (`gemini-2.5-flash`), Ollama (Local LLM)

---

## 🔨 Installation & Setup

### Prerequisite

1. Ensure **Python 3.10+** is installed on the device.
2. Setup Cloud API Keys OR install **Ollama**.

### 1. Configure Workspace Keys

Create & update `.env` file at the root:
```env
# Provider Settings (gemini, or ollama)
LLM_PROVIDER=gemini

# FastAPI / Backend Config
ENDEE_API_URL=http://localhost:8080
ENDEE_AUTH_TOKEN=

# Cloud API Keys
GEMINI_API_KEY=your_gemini_key_here

# Local LLM Config (if using 'ollama')
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma:latest
```

### 🟢 Using Local Offline LLM (Ollama)
1. Download from **[ollama.com](https://ollama.com)** and run the application.
2. Run: `ollama pull gemma:latest`
3. Update `.env` with `LLM_PROVIDER=ollama` + `OLLAMA_MODEL=gemma:latest`. 

---

### 2. Run Backend Setup

```bash
# Enter root of workspace
python -m venv venv
# Activate virtual environment
.\venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt

# [Optional] Seed Quiz questions database for static offline fallback
python backend/seed_quiz_pool.py

# Start Server
python backend/main.py
```

### 3. Open Frontend Layouts

Simply load **`http://localhost:8000/frontend/index.html`** or double click `frontend/index.html` file in your browser directly to load the Dashboard interactively!

---

## 🔌 Interface & API References

| Path | Method | Description |
|---|---|---|
| `/api/v1/materials/upload` | `POST` | Upload PDF files to index into node buffers |
| `/api/v1/assistant/ask` | `POST` | Ask questions with context loop queries (supports optional `sources: []` filter) |
| `/api/v1/materials/delete` | `POST` | Remove files and vector index bounds securely |
| `/api/v1/quiz/generate` | `POST` | Trigger MCQs pulling from Static DB fallbacks flawlessly |
| `/api/v1/translate` | `POST` | Core routing translating streams across selector ranges |

---

*Note: Verified running successfully in standard backgrounds triggers.*
