from typing import List, TypeVar, Generic, Type, Optional
import numpy as np
from config.database import db
from sqlalchemy.orm import Session
from sentence_transformers import CrossEncoder
from domain.models.documents_meta import DocumentMeta

T = TypeVar('T')

class BaseDocumentService(Generic[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
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
