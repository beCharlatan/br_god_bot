from typing import List, Dict, Optional
import numpy as np
from config.database import db
from sqlalchemy import func
from domain.models.document_embedding import DocumentEmbedding
from domain.models.file_embeddings import FileEmbeddings

class DocumentStore:
    def __init__(self):
        db.create_tables()
    
    def store_document_embedding(self, filename: str, content: str, embedding: List[float], original_filename: str):
        with next(db.get_db()) as session:
            # Get or create FileEmbeddings entry
            file_embedding = session.query(FileEmbeddings).filter_by(original_filename=original_filename).first()
            if not file_embedding:
                file_embedding = FileEmbeddings(original_filename=original_filename)
                session.add(file_embedding)
                session.flush()  # This will assign an id to file_embedding
            
            doc_embedding = DocumentEmbedding(
                filename=filename,
                content=content,
                embedding=str(embedding),
                file_embedding_id=file_embedding.id
            )
            session.add(doc_embedding)
            session.commit()
        
    def find_similar_documents(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        results = []
        with next(db.get_db()) as session:
            for doc in session.query(DocumentEmbedding).all():
                stored_embedding = np.array(eval(doc.embedding))
                similarity = np.dot(query_embedding, stored_embedding)
                results.append({
                    'filename': doc.filename,
                    'content': doc.content,
                    'similarity': similarity
                })
        
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]

    def get_document_id_by_name(self, filename: str) -> int | None:
        with next(db.get_db()) as session:
            document = session.query(FileEmbeddings).filter_by(original_filename=filename).first()
            return document.id if document else None

    def store_file_embeddings(self, filename: str, embeddings: List[List[float]]):
        with next(db.get_db()) as session:
            # Convert embeddings list to string representation
            embeddings_str = str(embeddings)
            
            # Check if entry exists
            existing = session.query(FileEmbeddings).filter_by(original_filename=filename).first()
            if existing:
                existing.embeddings = embeddings_str
            else:
                file_embeddings = FileEmbeddings(
                    original_filename=filename,
                    embeddings=embeddings_str
                )
                session.add(file_embeddings)
            session.commit()

    def get_all_documents(self) -> List[FileEmbeddings]:
        with next(db.get_db()) as session:
            return session.query(FileEmbeddings).all()
            
    def get_concatenated_embeddings(self, file_embedding_id: int, separator: str = ' ') -> Optional[str]:
        """
        Concatenate DocumentEmbedding embeddings filtered by file_embedding_id into a string using string_agg.
        
        Args:
            file_embedding_id (int): The ID of the FileEmbeddings to filter by
            separator (str): The separator to use between embeddings (default: space)
            
        Returns:
            Optional[str]: Concatenated string of embeddings or None if no embeddings found
        """
        with next(db.get_db()) as session:
            result = session.query(
                func.string_agg(DocumentEmbedding.content, separator)
            ).filter(
                DocumentEmbedding.file_embedding_id == file_embedding_id
            ).scalar()
            return result
