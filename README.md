# 🧠 AI-Powered Knowledge Base Search & Enrichment (Agentic RAG)

> A multi-agent Retrieval-Augmented Generation (RAG) system that lets users upload documents, query them in natural language, checks the completeness of answers, and suggests how to enrich the knowledge base when information is missing.

---

## 🚀 Overview

This project implements **Challenge 2** — *AI-Powered Knowledge Base Search & Enrichment*.  
It builds an **agentic RAG pipeline** using locally-run LLMs via **Ollama**, a vector store (**Qdrant**), and **FastAPI** as the orchestration layer.

Users can:
- Upload multiple documents (PDF, DOCX, TXT).  
- Ask natural-language questions.  
- Get grounded answers retrieved from the uploaded corpus.  
- See when the system is uncertain or incomplete.  
- Receive **structured enrichment suggestions** (e.g., *upload missing reports*, *connect data sources*, *fetch missing info*).  
- Benefit from **auto-enrichment** that fetches missing data from the web.  
- Provide binary feedback (**like / dislike**) to help improve the system.

---

## 🧩 System Architecture

```
 ┌────────────────────────┐
 │      FastAPI API       │
 │  /upload  /query /rate  │
 └──────────┬─────────────┘
            │
      ┌─────▼─────┐
      │ Orchestrator│ (LangGraph-style flow)
      └─────┬─────┘
            │
 ┌──────────┼─────────────────────────────────────────────┐
 │ Agents:                                                   │
 │ 1️⃣ Ingestion Agent  – parses docs → chunks → embeddings   │
 │ 2️⃣ Retrieval Agent  – fetches top-k context chunks        │
 │ 3️⃣ Answering Agent  – grounded LLM answer                 │
 │ 4️⃣ Completeness Agent – checks if info sufficient          │
 │ 5️⃣ Enrichment Agent – suggests upload/connect/fetch actions│
 │ 6️⃣ Auto-Fetcher – actually fetches data if “fetch” action  │
 │ 7️⃣ Rating Endpoint – logs like/dislike feedback            │
 └──────────────────────────────────────────────────────────┘
            │
      ┌─────▼─────┐
      │ Qdrant DB │ ← embeddings from sentence-transformers
      └───────────┘
            │
      ┌─────▼─────┐
      │ Ollama LLM│ (llama3 / mistral / phi3 etc.)
      └───────────┘
```

---

## 🧠 Design Decisions

| Area | Decision | Reason |
|------|-----------|--------|
| **LLM Runtime** | Local **Ollama** (default `llama3`) | 100 % offline, avoids API keys |
| **Framework** | **FastAPI** for orchestration | Lightweight, async, well-documented |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` | Fast, 384-dim vector size, fits 8 GB RAM |
| **Vector Store** | **Qdrant** (local mode) | High-performance, easy integration |
| **Orchestration Pattern** | Multi-agent (LangGraph-like state machine) | Clear separation of roles, debuggable |
| **Output Format** | Structured JSON (`answer`, `confidence`, `completeness`, `missing_info`, `enrichment_actions`, `auto_fetched_data`) | Enables downstream automation |
| **Error Handling** | Each agent sanitizes LLM output → JSON-safe fallback | Prevents pipeline crashes |
| **Auto-Enrichment** | Simple web fetcher (DuckDuckGo/Wikipedia) | Demonstrates concept without external keys |
| **User Feedback** | `/api/rate` with **binary like/dislike feedback** | Simpler, intuitive feedback mechanism |

---

## ⚖️ Trade-Offs (24 h Implementation Constraint)

| Area | Trade-Off | Rationale |
|------|------------|------------|
| **Frontend** | Streamlit UI for upload, search, rating | Lightweight local dashboard that complements the API |
| **Security / Auth** | No user auth | Simplified local demo |
| **Scalability** | Single-process FastAPI | Sufficient for local prototype |
| **Retrieval** | Basic top-k cosine | Enough to show end-to-end RAG flow |
| **Evaluation Loop** | Feedback stored, not used live | Keeps feedback loop lightweight |
| **LLM Output Validation** | Enforced structured JSON via fallback | Handles Ollama’s non-deterministic output |

---

## 🧰 Setup & Running Locally

### 1️⃣ Clone Repo & Setup Environment
```bash
git clone https://github.com/<your-username>/ai-knowledge-base.git
cd ai-knowledge-base
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2️⃣ Install & Run Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3         # or mistral / llama3
ollama serve
```
*(If port 11434 is busy → `OLLAMA_HOST=127.0.0.1:11500 ollama serve`)*

### 3️⃣ Set Environment Variables
Copy the example:
```bash
cp .env.example .env
```

`.env`
```env
LLM_MODEL=llama3
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=./data/qdrant
COLLECTION_NAME=knowledge_base
```

### 4️⃣ Run the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open Swagger → **http://127.0.0.1:8000/docs**

### 5️⃣ Run the Streamlit UI
```bash
streamlit run frontend/streamlit_app.py
```

---

## 🧪 How to Test the System

1. **Upload a document**
   - `POST /api/upload`  
     Upload a PDF/DOCX/TXT (e.g., *Coordination Compounds* chapter).

2. **Ask a question**
   - `POST /api/query`
   ```json
   {
     "text": "What are coordination compounds?"
   }
   ```

3. **View the structured output**
   ```json
   {
     "answer": "Coordination compounds are ...",
     "confidence": 0.8,
     "completeness": "HIGH",
     "missing_info": [],
     "enrichment_actions": [
       { "type": "fetch", "label": "Fetch examples of coordination compounds" }
     ],
     "auto_fetched_data": [
       { "query": "Fetch examples of coordination compounds", "data": "Introductory overview of common coordination compounds ..." }
     ],
     "orchestration_trace": ["RETRIEVING","ANSWERING","CHECKING_COMPLETENESS","ENRICHMENT"]
   }
```

4. **Rate the answer**
   - `POST /api/rate`
   ```json
   {
     "question": "What are coordination compounds?",
     "answer": "Coordination compounds are ...",
     "rating": "like",
     "comments": "Accurate and helpful."
   }
   ```
   or
   ```json
   {
     "question": "What are coordination compounds?",
     "answer": "It missed examples.",
     "rating": "dislike",
     "comments": "Incomplete explanation."
   }
   ```

5. **Check feedback logs**
   - File: `data/feedback/ratings.jsonl`

---

## 🌱 Auto-Enrichment Example

When the Enrichment Agent suggests:
```json
{ "type": "fetch", "label": "Fetch Q3 2025 financial summary" }
```
the orchestrator automatically calls the internal fetcher (DuckDuckGo (default), can be modified to use Wikipedia API or any other source)  
→ retrieves data → appends it to the final answer and exposes the snippet via `auto_fetched_data` for the UI.

---

## 🪶 Example Response Flow

```
RETRIEVING        →  top-5 relevant chunks
ANSWERING         →  grounded LLM answer (Ollama)
CHECK_COMPLETENESS→  validates coverage (JSON)
ENRICHMENT        →  suggests upload/connect/fetch actions
AUTO_ENRICHMENT   →  optional live fetch
DONE              →  aggregated structured JSON output
```

---

## 📚 Folder Structure

```
ai-knowledge-base/
├── app/
│   ├── main.py
│   ├── routes/          → upload, query, rate
│   ├── orchestrator/
│   │   ├── agents/      → individual agent scripts
│   │   ├── utils/       → llm, embeddings, storage, fetcher
│   │   └── orchestrator.py
│   └── schemas.py
├── data/                → uploads, qdrant, feedback
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

## 🧠 Future Improvements

- ✅ Replace heuristic retrieval with **hybrid retriever** (dense + BM25)  
- ✅ Integrate **LangGraph** for visual orchestration  
- ✅ Use **feedback analytics** to improve enrichment prompts  
- ✅ Add **frontend dashboard** for progress visualization  
- ✅ Fine-tune local model for better JSON compliance  

---

**Author:** Rahul Singh  
**Built with:** FastAPI · Ollama · LangChain-style Agents · Qdrant  
