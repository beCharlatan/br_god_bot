from typing import List, Dict, TypeVar, Generic
from langchain_text_splitters import CharacterTextSplitter
from services.embeddings.gigachat_embeddings import GigaChatEmbeddings
from services.documents.base_document_service import BaseDocumentService
from concurrent.futures import ThreadPoolExecutor

T = TypeVar('T')

class BaseDocumentEmbedder(Generic[T]):
    def __init__(self, document_service: BaseDocumentService[T]):
        self.document_service = document_service
        self.embeddings = GigaChatEmbeddings()
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=300,
            chunk_overlap=50,
            length_function=len
        )
    
    # TODO: добавить многопоточность (одновременно можно процессить в 3х потоках)
    def process_document(self, content: str, document_meta_id: int) -> List[float]:
        """Process document content, store embeddings, and return document embedding."""
        chunks = self.text_splitter.split_text(content)
        
        chunk_embeddings = []
        
        def process_chunk(chunk):
            chunk_embedding = self.embeddings.create_embedding(chunk)
            self.document_service.store_document_embedding(chunk, chunk_embedding, document_meta_id)
            return chunk_embedding
        
        with ThreadPoolExecutor(max_workers=1) as executor:
            chunk_embeddings = list(executor.map(process_chunk, chunks))
        
        return chunk_embeddings[0] if chunk_embeddings else []
    
    def find_similar_documents(self, query_text: str, bi_encoder_limit: int = 10, final_limit: int = 3) -> List[Dict]:
        """Find similar documents using two-stage retrieval."""
        query_embedding = self.embeddings.create_embedding(query_text)
        return self.document_service.find_similar_documents(
            query_embedding=query_embedding,
            query_text=query_text,
            bi_encoder_limit=bi_encoder_limit,
            final_limit=final_limit
        )
