# Fast Insight Retriever

A high-performance RAG (Retrieval-Augmented Generation) web application tailored for documentation QA. It features a scalable vector search (Qdrant), LLM integration (vLLM/Llama-3), and a responsive UI.

## 🚀 Features

- **Document Ingestion:** Parses PDFs/Text, chunks, and embeds them into Qdrant.
- **High-Speed RAG:** Uses `vLLM` for fast inference and `Qdrant` with HNSW indexing.
- **Secure Auth:** Flask-Login with hashed passwords.
- **Responsive UI:** Mobile-first design using Tailwind CSS.
- **Scalable:** Dockerized, with Redis caching support.

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
