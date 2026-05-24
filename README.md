# 📄 PDF Summarizer AI

A FastAPI-based service that allows users to upload PDF documents and receive AI-generated summaries using OpenAI models. The system processes documents asynchronously, stores results in PostgreSQL, and provides a simple web UI to track processing status.

---

## 🚀 Features

- 📤 Upload PDF files (up to configurable size limit)
- 🤖 AI-powered summarization using OpenAI
- ⚡ Asynchronous background processing
- 🗄 PostgreSQL storage for file metadata and results
- 📊 Track processing status (pending / processing / done / failed)
- 🌐 Simple web UI (Jinja2 templates)
- 📜 View last uploaded documents
- 🐳 Dockerized setup (backend + database)

---

## 📦 Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Jinja2 (UI)
- OpenAI API
- Docker & Docker Compose

---

## ⚙️ Setup

### 1. Clone project

```bash
git clone https://github.com/RomanHlodann/summary_ai.git
cd summary_ai
```

### 2. Environment variables

Create `.env` file, for example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app
OPENAI_API_KEY=OPENAI_API_KEY
```

### 3. Run with Docker

```bash
docker compose up --build
```

The only page will be available at: http://localhost:8000

Swagger at: http://localhost:8000/docs



## 📡 API Endpoints

### Upload PDF
POST /summarize

Form-data:
- file: PDF file

Response:
```json
{
  "file_id": 1,
  "status": "pending"
}
```

---

### Get last uploads
GET /history

---

### Health check
GET /health

---

## 🌐 Web UI

GET /

Features:
- upload PDF
- view last 5 documents

---

## 🔄 Processing Flow

1. Upload PDF
2. Parse document into pages
3. Chunk pages
4. Generate summary with OpenAI
5. Save result in DB

---

## 🧠 Future Improvements

- Celery / Redis queue instead of BackgroundTasks
- WebSocket live updates
- Token-based chunking with overlap
- Authentication
- Pagination for history
- File duplication check
