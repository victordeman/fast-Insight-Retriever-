import pytest
from unittest.mock import MagicMock
from rag import RAGEngine

@pytest.fixture
def rag():
    # Mock dependencies to test logic without needing a running Qdrant/GPU
    engine = RAGEngine()
    engine.qdrant = MagicMock()
    engine.encoder = MagicMock()
    engine.llm = MagicMock()
    # Mock embedding return
    engine.encoder.encode.return_value.tolist.return_value = [0.1, 0.2, 0.3]
    return engine

def test_rag_query_flow(rag):
    # Mock Search Result
    hit_mock = MagicMock()
    hit_mock.payload = {'page_content': 'Test context info'}
    rag.qdrant.search.return_value = [hit_mock]
    
    # Mock LLM generation
    output_mock = MagicMock()
    output_mock.outputs[0].text = "Test Answer"
    rag.llm.generate.return_value = [output_mock]
    
    response = rag.rag_query("What is X?")
    assert "Test Answer" == response
    rag.qdrant.search.assert_called_once()
