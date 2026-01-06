import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from config import Config

def ingest_documents():
    print(f"🚀 Starting ingestion from {Config.DOCS_PATH}...")
    
    # 1. Load Documents
    if not os.path.exists(Config.DOCS_PATH):
        os.makedirs(Config.DOCS_PATH)
        print("Created docs directory. Please add files.")
        return

    loader = DirectoryLoader(Config.DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
    # Fallback for text files
    txt_loader = DirectoryLoader(Config.DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader)
    
    docs = loader.load() + txt_loader.load()
    print(f"Loaded {len(docs)} documents.")

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    chunks = text_splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    # 3. Embed
    encoder = SentenceTransformer(Config.EMBEDDING_MODEL)
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    
    print("Embedding chunks (this may take a while)...")
    embeddings = encoder.encode(texts, show_progress_bar=True)

    # 4. Store in Qdrant
    client = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
    
    # Recreate collection to ensure fresh start
    client.recreate_collection(
        collection_name=Config.COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

    # Upsert in batches
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        end = min(i + batch_size, len(chunks))
        
        points = []
        for j in range(i, end):
            points.append({
                'id': j,
                'vector': embeddings[j].tolist(),
                'payload': {
                    'page_content': texts[j],
                    'source': metadatas[j].get('source', 'unknown')
                }
            })
            
        client.upsert(
            collection_name=Config.COLLECTION_NAME,
            points=points
        )
        print(f"Uploaded batch {i} - {end}")

    print("✅ Ingestion complete.")

if __name__ == "__main__":
    ingest_documents()
