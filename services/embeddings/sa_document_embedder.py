from typing import List, Dict
from services.embeddings.base_document_embedder import BaseDocumentEmbedder
from services.documents.sa_document_service import SADocumentService
from domain.models.sa_document_embedding import SADocumentEmbedding

class SADocumentEmbedder(BaseDocumentEmbedder[SADocumentEmbedding]):
    def __init__(self):
        super().__init__(SADocumentService())

    def process_document(self, content: str, document_meta_id: int) -> List[float]:
        """Process document content and create embeddings."""
        return super().process_document(content, document_meta_id)

    def find_similar_sa_documents(self, query_text: str, bi_encoder_limit: int = 10, final_limit: int = 3) -> List[Dict]:
        """Find similar SA documents using two-stage retrieval."""
        return self.find_similar_documents(
            query_text=query_text,
            bi_encoder_limit=bi_encoder_limit,
            final_limit=final_limit
        )
