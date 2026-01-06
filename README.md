# Fast Insight Retriever

A high-performance RAG (Retrieval-Augmented Generation) web application tailored for documentation QA. It features a scalable vector search (Qdrant), LLM integration (vLLM/Llama-3), and a responsive UI.

## 🚀 Features

- **Document Ingestion:** Parses PDFs/Text, chunks, and embeds them into Qdrant.
- **High-Speed RAG:** Uses `vLLM` for fast inference and `Qdrant` with HNSW indexing.
- **Secure Auth:** Flask-Login with hashed passwords.
- **Responsive UI:** Mobile-first design using Tailwind CSS.
- **Scalable:** Dockerized, with Redis caching support.

## Repository Structure

```
fast-Insight-Retriever/
├── app.py                   # Main Flask app
├── rag.py                   # RAG logic (Qdrant + vLLM)
├── ingest.py                # Document ingestion pipeline
├── requirements.txt         # Dependencies
├── Dockerfile               # Application container
├── docker-compose.yml       # Services (App + Qdrant + Redis)
├── .gitignore               # Git ignore rules
├── README.md                # Documentation
├── config.py                # Configuration management
├── .env.example             # Environment variable template
├── templates/
│   ├── index.html           # Main Chat Interface
│   └── login.html           # Login Interface
├── static/
│   └── js/
│       └── app.js           # Frontend Logic
└── tests/
    ├── test_rag.py
    └── test_app.py
```

## 🛠️ Setup

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- (Optional) NVIDIA GPU for vLLM acceleration.

### Quick Start (Local)

1. **Clone the Repo**
   ```bash
   git clone [https://github.com/victordeman/fast-Insight-Retriever-.git](https://github.com/victordeman/fast-Insight-Retriever-.git)
   cd fast-Insight-Retriever

## 🛠️ Environment Setup

2. **Clone the Repo**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env

## Start Infrastructure (Qdrant & Redis)

3. **Clone the Repo**
   ```bash
   docker-compose up -d qdrant redis

## Ingest Documents Place your PDFs in data/docs/ and run:

4. **Clone the Repo**
   ```bash
   python ingest.py

## Ingest Documents Place your PDFs in data/docs/ and run:

5. **Clone the Repo**
   ```bash
   # Initialize DB (Run once)
   python -c "from app import setup; print(setup())"

   # Start Server
   python app.py



   
