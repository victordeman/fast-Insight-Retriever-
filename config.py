import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # RAG Settings
    QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
    QDRANT_COLLECTION = os.getenv('QDRANT_COLLECTION', 'fast_insight_docs')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    LLM_MODEL_PATH = os.getenv('LLM_MODEL_PATH', 'meta-llama/Llama-2-7b-chat-hf') # Adjust for Llama-3 if available locally
    
    # Toggle for development on non-GPU machines
    USE_MOCK_LLM = os.getenv('USE_MOCK_LLM', 'False').lower() == 'true'

  
    DOCS_PATH = os.getenv('DOCS_PATH', 'data/docs')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
