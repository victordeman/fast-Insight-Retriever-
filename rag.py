import time
from typing import List, Optional
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from config import Config
import redis
import json

# Try importing vLLM, handle graceful fallback for non-GPU environments during build
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False
    print("WARNING: vLLM not found. Ensure you are on Linux with CUDA.")

class RAGEngine:
    def __init__(self):
        # Initialize Vector DB Client
        self.qdrant = QdrantClient(host=Config.QDRANT_HOST, port=Config.QDRANT_PORT)
        
        # Initialize Embedding Model (CPU optimized for small models)
        self.encoder = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Initialize Cache
        self.cache = redis.from_url(Config.REDIS_URL) if Config.ENABLE_CACHE else None
        
        # Initialize LLM
        self.llm = None
        self.sampling_params = None
        if VLLM_AVAILABLE:
            # Load Llama-3-8B (Assuming GPU available)
            # Note: In production, this usually runs as a separate API server 
            # to avoid blocking Flask workers. For this standalone repo, we load it here.
            try:
                self.llm = LLM(model="meta-llama/Meta-Llama-3-8B-Instruct", trust_remote_code=True)
                self.sampling_params = SamplingParams(temperature=0.1, max_tokens=200)
            except Exception as e:
                print(f"Failed to load vLLM: {e}")

    def embed_text(self, text: str) -> List[float]:
        return self.encoder.encode(text).tolist()

    def search_context(self, query_vector: List[float], top_k: int = 5) -> str:
        hits = self.qdrant.search(
            collection_name=Config.COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )
        return "\n\n".join([hit.payload['page_content'] for hit in hits])

    def rag_query(self, query: str) -> str:
        start_time = time.time()
        
        # 1. Check Cache
        if self.cache:
            cached = self.cache.get(query)
            if cached:
                return json.loads(cached)['response']

        # 2. Retrieve
        vector = self.embed_text(query)
        context = self.search_context(vector)
        
        if not context:
            return "I couldn't find any relevant documents to answer your question."

        # 3. Augment & Generate
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a precise assistant. Answer the question based ONLY on the context provided.
Context:
{context}
<|eot_id|><|start_header_id|>user<|end_header_id|>
Question: {query}
Answer:<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        if self.llm:
            outputs = self.llm.generate([prompt], self.sampling_params)
            answer = outputs[0].outputs[0].text.strip()
        else:
            answer = "[Mock Response] vLLM not loaded. Context found: " + context[:100] + "..."

        # 4. Cache Result
        if self.cache:
            self.cache.setex(query, 3600, json.dumps({'response': answer}))

        print(f"Query processed in {time.time() - start_time:.4f}s")
        return answer

# Singleton instance
rag_engine = RAGEngine()
