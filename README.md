# 🚀 AI Study Assistant

A production-ready, AI-powered learning platform leveraging **Retrieval-Augmented Generation (RAG)**, semantic search, and interactive voice integration. Upload materials, interact with local or cloud models, and generating instant smart quizzes flawlessly.

---

## 🌟 Features

- **🧠 Dashboard**: Comprehensive overview displaying overall study statistics and quick action cards in a sleek design.
- **💬 Chat Assistant**: Real-time conversational AI answering queries using context extracted from uploaded documents (Ollama or Google Gemini backed).
- **📂 Upload PDF**: Drag & Drop indexing of long-form academic papers, processing content efficiently.
- **📄 Documents Management**: View listed uploads, filter items, and delete stale context nodes flawlessly.
- **🧠 Quiz System**: Dynamic multiple-choice question generator adapting to specific domains with failover offline question-pools.
- **🌐 Translator**: Translate AI answer frames into languages target nodes securely on the fly.
- **🎤 Voice AI**: Speak-to-prompt inputs binding speech-recognition and text-to-speech triggers natively.

---

## 🧠 How It Works (RAG Pipeline)

The AI Study Assistant follows an advanced **Retrieval-Augmented Generation** workflow to ensure accuracy and prevent hallucinations:

1. **PDF Upload & Extraction**: PDFs are processed to extract raw textual sequences securely.
2. **Chunking & Embedding Generation**: Extracted nodes are chunked and transformed into vector embeddings.
3. **Storage in Endee Vector DB**: Embeddings are indexed into the **Endee Vector Database** for sub-second retrieval times.
4. **Semantic Context Retrieval**: When you query the assistant, the system computes similarity matrices against the Vector DB.
5. **LLM Inference Responses**: Retrieved context streams into the LLM (Ollama / Gemini) to produce hyper-accurate, sourced answers absolute safely.

---

## ⚙️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Frontend**: Vanilla HTML5, CSS3 Glassmorphism, Modern JavaScript
- **Vector Database**: Endee Vector DB
- **LLM Integrations**: [Google Gemini](https://ai.google.dev/) (Default) & [Ollama](https://ollama.com/) (Local Fallback)

---

## 📂 Project Structure

```text
├── backend/               # FastAPI route handlers, logic, and RAG pipelines
├── frontend/              # Sleek Glassmorphic HTML page assets and JS views
├── requirements.txt       # Core Python library dependencies list
└── .env                   # Configuration mapping APIs and model triggers
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/assistant/ask` | `POST` | Query the Assistant with RAG context routing. |
| `/api/v1/materials/upload` | `POST` | Index document textual buffers into Endee. |
| `/api/v1/materials/delete` | `POST` | Wipe file bindings and vector bounds flawlessly. |
| `/api/v1/quiz/generate` | `POST` | Trigger smart MCQs with fall-proof failovers. |
| `/api/v1/translate` | `POST` | Core Routing parsing translated buffers. |

---

## 🛠️ Installation & Setup

### 1. Clone the Workspace
```bash
git clone https://github.com/sonukumarji7479/endee.git
cd endee
```

### 2. Set Up Environment variables
Create a `.env` file in the workspace root with target API keys:
```env
LLM_PROVIDER=gemini  # Or 'ollama'
GEMINI_API_KEY=your_gemini_api_key_here
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=gemma:latest
```

---

## ▶️ Run Locally

Provide running orders:

```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Backend Server
python backend/main.py
```

Load **`http://localhost:8000/frontend/index.html`** in your browser to view Dashboard triggers interactively.

---

## 📸 Screenshots

*Place screenshot asset nodes here.*

---

## 🚀 Live Demo

[Explore Live Instance (Placeholder)]()

---

## 🌐 Future Scope

- 📱 **Mobile App Interface**: React Native layouts.
- ☁️ **Cloud Deployment**: Containerized hosting pipelines.
- 🔑 **User Authentication**: Secure workspace session filters.
- 🤝 **Real-Time Collaboration**: Shareable notebooks layouts.

---

## 👨‍💻 Author

**Sonu Kumar** ([@sonukumarji7479](https://github.com/sonukumarji7479))
