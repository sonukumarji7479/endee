# 🚀 AI Study Assistant
> **A production-ready AI-powered learning platform using RAG, semantic search, and voice intelligence.**

---

## 📖 Description

The **AI Study Assistant** is a premium learning platform leveraging **Retrieval-Augmented Generation (RAG)**, semantic search, and interactive voice intelligence. Upload complex documents (PDFs), ask context-aware questions with AI assistants, and generate smart quizzes absolute flawlessly to transform absolute study flows streamingly.

---

## 🌟 Features (Enhanced)

- **🧠 Dashboard**: Intelligent overview displaying comprehensive analytics statistics and quick action drawer triggers in a sleek responsive layout.
- **💬 Chat Assistant**: Context-aware AI response streams leveraging either **Google Gemini** or **Ollama (local)** to output hyper-accurate data absolute cleanly.
- **📂 Upload PDF**: Drag & drop document indexing extraction extracting textual sequences securely.
- **📄 Documents Management**: View listed uploads index buffers, filter items relative offsets securely, and wipe stale files flaws flawlessly.
- **🧠 Quiz System**: Smart MCQ generator with infinite limits adaptive strictly utilizing fallback cached question-pools to ensure 100% offline uptime securely.
- **🌐 Translator**: Multi-language support to translate AI response frames synchronously.
- **🎤 Voice AI**: Speak-to-prompt controls incorporating Native Speech-to-Text (STT) and Text-to-Speech (TTS) bindings cleanly.

---

## 🧠 How It Works (RAG Pipeline)

The AI Study Assistant utilizes an advanced, scalable **Retrieval-Augmented Generation** absolute layout workflow to prevent hallucinations and maintain absolute source integrity:

1. **PDF Upload & Text Extraction**: Long-form paper materials are parsed into raw textual strings securely.
2. **Chunking & Embedding Generation**: Nodes are chunked and transformed into high-density vector embeddings absolute cleanly.
3. **Storage in Endee Vector Database**: Embedded sequences index into the **Endee Vector Database** for sub-second retrieval benchmarks.
4. **Semantic Context Retrieval**: When you query the platform, parallel similarity checks pull only the most relevant materials out of absolute indexes.
5. **LLM Response Generation**: Sourced contexts stream into the LLM (Ollama / Gemini) to produce hyper-accurate responses securely.

---

## ⚙️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Frontend**: Vanilla HTML5, CSS3 Glassmorphism UI Layouts, Modern JavaScript
- **Vector Database**: Endee Vector DB
- **LLM Integrations**: [Google Gemini](https://ai.google.dev/) (Default) & [Ollama](https://ollama.com/) (Local Fallback)

---

## 📂 Project Structure

```text
├── backend/               # FastAPI API endpoints, routers, and RAG pipelines
├── frontend/              # Sleek Glassmorphic UI pages layouts + script loaders
├── requirements.txt       # Core Python library dependencies list
└── .env                   # Configuration mapping APIs and model triggers
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/assistant/ask` | `POST` | Query AI with RAG context routing absolute securely. |
| `/api/v1/materials/upload` | `POST` | Index document textual buffers into Endee. |
| `/api/v1/materials/delete` | `POST` | Delete files and document nodes flawlessly. |
| `/api/v1/quiz/generate` | `POST` | Generate adaptive MCQs securely. |
| `/api/v1/translate` | `POST` | Translate text sequences synchronously. |

---

## 🛠️ Installation & Setup

1. **Clone the Workspace**
   ```bash
   git clone https://github.com/sonukumarji7479/endee.git
   cd endee
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the root directory:
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

Open **`http://localhost:8000/frontend/index.html`** inside your browser to interact with the Dashboard natively absolute smoothly!

---

## 🚀 Live Demo

🌐 [Explore Live Instance](https://aistudentpartner.netlify.app)

---

## 📸 Screenshots

*Place screenshot asset nodes here.*

---

## 🌐 Future Scope

- 📱 **Mobile App Control**: Dedicated scaling frameworks.
- ☁️ **Cloud Deployment container templates**.
- 🔑 **User Authentication filters**.
- 🤝 **Real-Time Collaboration tools**.

---

## 👨‍💻 Author

**Sonu Kumar** ([@sonukumarji7479](https://github.com/sonukumarji7479))
