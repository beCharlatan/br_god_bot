from typing import List, TypeVar, Generic, Type, Optional, Dict
import numpy as np
from config.database import db
from sqlalchemy.orm import Session
from sentence_transformers import CrossEncoder
from domain.models.documents_meta import DocumentMeta
from abc import ABC, abstractmethod

T = TypeVar('T')

class BaseDocumentService(Generic[T], ABC):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    @abstractmethod
    def _bi_encoder_retrieval(self, query_embedding: List[float], query_text: str, session: Session) -> List[Dict]:
        """Retrieve documents using bi-encoder similarity.
        Returns list of dicts with 'content', 'similarity', and other relevant fields."""
        pass

    @abstractmethod
    def _cross_encoder_reranking(self, candidates: List[Dict], query_text: str, limit: int) -> List[Dict]:
        """Rerank documents using cross-encoder.
        Returns reranked list of dicts with additional 'cross_encoder_score' field."""
        pass

    def find_similar_documents(self, query_embedding: List[float], query_text: str,
                             bi_encoder_limit: int = 10, final_limit: int = 3) -> List[Dict]:
        """Pipeline for finding similar documents using two-stage retrieval."""
        try:
            with self._get_session() as session:
                # Stage 1: Bi-encoder retrieval
                bi_encoder_results = self._bi_encoder_retrieval(query_embedding, query_text, session)
                if not bi_encoder_results:
                    print("No valid results found in bi-encoder stage")
                    return []

                # Get top-k results from bi-encoder
                bi_encoder_results.sort(key=lambda x: x['similarity'], reverse=True)
                top_candidates = bi_encoder_results[:bi_encoder_limit]

                try:
                    # Stage 2: Cross-encoder reranking
                    final_results = self._cross_encoder_reranking(top_candidates, query_text, final_limit)
                    return final_results
                except Exception as e:
                    print(f"Error during cross-encoder reranking: {str(e)}")
                    return top_candidates[:final_limit]

        except Exception as e:
            print(f"Error in find_similar_documents: {str(e)}")
            return []
    
    def _get_session(self) -> Session:
        return db.SessionLocal()
    
    def _calculate_similarity(self, query_embedding: List[float], stored_embedding: List[float]) -> float:
        """Calculate similarity between query and stored embeddings."""
        return float(np.dot(query_embedding, stored_embedding))
    
    def _parse_embedding(self, embedding_str: str) -> List[float]:
        """Parse embedding string to list of floats."""
        try:
            return eval(embedding_str)
        except Exception as e:
            print(f"Error parsing embedding: {str(e)}")
            return []
    
    def get_document_meta_by_title(self, title: str) -> Optional[DocumentMeta]:
        """Get document metadata by title."""
        with self._get_session() as session:
            return session.query(DocumentMeta).filter(DocumentMeta.title == title).first()
