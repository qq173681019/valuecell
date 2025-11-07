from pathlib import Path
from typing import Optional

from agno.knowledge.chunking.markdown import MarkdownChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.reader.pdf_reader import PDFReader

from .vdb import vector_db

# Create knowledge base with error handling for disabled embeddings
try:
    knowledge = Knowledge(
        vector_db=vector_db,
        max_results=10,
    )
    md_reader = MarkdownReader(chunking_strategy=MarkdownChunking())
    pdf_reader = PDFReader(chunking_strategy=MarkdownChunking())
except Exception as e:
    print(f"Warning: Knowledge base initialization failed ({e}). Document search will be disabled.")
    # Create mock knowledge base
    class MockKnowledge:
        async def search_async(self, *args, **kwargs):
            return []
        
        def search(self, *args, **kwargs):
            return []
        
        async def add_content_async(self, *args, **kwargs):
            pass
    
    knowledge = MockKnowledge()
    md_reader = None
    pdf_reader = None


async def insert_md_file_to_knowledge(
    name: str, path: Path, metadata: Optional[dict] = None
):
    if md_reader is None:
        print("Warning: Document insertion disabled - embeddings not available")
        return
    await knowledge.add_content_async(
        name=name,
        path=path,
        metadata=metadata,
        reader=md_reader,
    )


async def insert_pdf_file_to_knowledge(url: str, metadata: Optional[dict] = None):
    if pdf_reader is None:
        print("Warning: Document insertion disabled - embeddings not available")
        return
    await knowledge.add_content_async(
        url=url,
        metadata=metadata,
        reader=pdf_reader,
    )
