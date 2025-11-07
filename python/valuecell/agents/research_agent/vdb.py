"""
Vector database configuration for Research Agent.

This module uses the centralized configuration system to create an embedder
and vector database. It automatically:
1. Selects an available provider with embedding support (OpenAI, SiliconFlow, etc.)
2. Uses the provider's API key from .env
3. Falls back to other providers if the primary fails
4. Respects environment variable overrides (EMBEDDER_MODEL_ID, EMBEDDER_DIMENSION)

Configuration Priority (highest to lowest):
1. Environment Variables (EMBEDDER_MODEL_ID, EMBEDDER_DIMENSION, etc.)
2. .env file (OPENROUTER_API_KEY, SILICONFLOW_API_KEY, etc.)
3. YAML files (configs/agents/research_agent.yaml, configs/providers/*.yaml)
"""

from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

import valuecell.utils.model as model_utils_mod
from valuecell.utils.db import resolve_lancedb_uri

# Try to create embedder, but provide fallback if embeddings are disabled
try:
    # Create embedder using the configuration system
    # This will:
    # - Check EMBEDDER_MODEL_ID env var first
    # - Auto-select provider with embedding support (e.g., SiliconFlow if SILICONFLOW_API_KEY is set)
    # - Use provider's default embedding model if not specified
    # - Fall back to other providers if primary fails
    embedder = model_utils_mod.get_embedder_for_agent("research_agent")
    
    # Create vector database with the configured embedder
    vector_db = LanceDb(
        table_name="research_agent_knowledge_base",
        uri=resolve_lancedb_uri(),
        embedder=embedder,
        # reranker=reranker,  # Optional: can be configured later, reranker config in modelprovider yaml file if needed
        search_type=SearchType.hybrid,
        use_tantivy=False,
    )
except Exception as e:
    print(f"Warning: Embeddings disabled or unavailable ({e}). Knowledge base search will be disabled.")
    # Create a mock vector_db that returns empty results
    class MockVectorDb:
        async def search_async(self, *args, **kwargs):
            return []
        
        def search(self, *args, **kwargs):
            return []
            
        async def upsert_async(self, *args, **kwargs):
            pass
            
        def upsert(self, *args, **kwargs):
            pass
    
    vector_db = MockVectorDb()
