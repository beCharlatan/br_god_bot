from typing import List, Dict, Optional
from services.embeddings.base_document_embedder import BaseDocumentEmbedder
from services.documents.ba_document_service import BADocumentService
from domain.models.ba_document_embedding import BADocumentEmbedding

class BADocumentEmbedder(BaseDocumentEmbedder[BADocumentEmbedding]):
    def __init__(self):
        super().__init__(BADocumentService())

    def process_document(self, content: str, document_meta_id: int) -> List[float]:
        """Process document content and create embeddings."""
        return super().process_document(content, document_meta_id)

    def find_similar_ba_documents(self, query_text: str, bi_encoder_limit: int = 10, final_limit: int = 3) -> List[Dict]:
        """Find similar BA documents using two-stage retrieval."""
        return self.find_similar_documents(
            query_text=query_text,
            bi_encoder_limit=bi_encoder_limit,
            final_limit=final_limit
        )
