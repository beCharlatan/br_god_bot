from typing import List, Dict
from domain.models.ba_document_embedding import BADocumentEmbedding
from services.documents.base_document_service import BaseDocumentService
from sqlalchemy.orm import Session

class BADocumentService(BaseDocumentService[BADocumentEmbedding]):
    def __init__(self):
        super().__init__(BADocumentEmbedding)
    
    def store_document_embedding(self, content: str, embedding: List[float], document_meta_id: int) -> None:
        """Store BA document embedding."""
        with self._get_session() as session:
            doc_embedding = BADocumentEmbedding(
                content=content,
                embedding=str(embedding),
                document_meta_id=document_meta_id
            )
            session.add(doc_embedding)
            session.commit()
    
    def _bi_encoder_retrieval(self, query_embedding: List[float], query_text: str, session: Session) -> List[Dict]:
        """Retrieve documents using bi-encoder similarity."""
        bi_encoder_results = []
        
        from sqlalchemy import text
        # Join с таблицей метаданных для получения ссылки на confluence
        documents = session.query(self.model_class, text('documents_meta.ba_document_confluence_link')).\
            join('document_meta').all()
        if not documents:
            print("Warning: No BA documents found in the database")
            return []

        for doc, confluence_link in documents:
            try:
                stored_embedding = self._parse_embedding(doc.embedding)
                if len(stored_embedding) != len(query_embedding):
                    print(f"Warning: Skipping document due to embedding dimension mismatch")
                    continue

                similarity = self._calculate_similarity(query_embedding, stored_embedding)
                bi_encoder_results.append({
                    'content': doc.content,
                    'similarity': similarity,
                    'confluence_link': confluence_link
                })
            except Exception as e:
                print(f"Error processing document: {str(e)}")
                continue

        return bi_encoder_results

    def _cross_encoder_reranking(self, candidates: List[Dict], query_text: str, limit: int) -> List[Dict]:
        """Rerank documents using cross-encoder."""
        # Prepare inputs for cross-encoder
        cross_encoder_inputs = [(query_text, doc['content']) for doc in candidates]
        cross_scores = self.cross_encoder.predict(cross_encoder_inputs)

        # Combine results with cross-encoder scores
        for idx, score in enumerate(cross_scores):
            candidates[idx]['cross_encoder_score'] = float(score)

        # Sort by cross-encoder scores and return top results
        final_results = sorted(candidates, key=lambda x: x['cross_encoder_score'], reverse=True)
        return final_results[:limit]
