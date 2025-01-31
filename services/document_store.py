from typing import List, Dict
import numpy as np
from config.database import db
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

    def get_document_embeddings_by_file(self, filename: str) -> List[Dict]:
        """
        Get all document embeddings associated with a specific file.
        
        Args:
            filename (str): The original filename to look up
            
        Returns:
            List[Dict]: List of dictionaries containing document embedding records with
                       'filename', 'content', and 'embedding' keys
        """
        with next(db.get_db()) as session:
            file_embedding = session.query(FileEmbeddings).filter_by(original_filename=filename).first()
            if file_embedding:
                return [{
                    'filename': doc.filename,
                    'content': doc.content,
                    'embedding': eval(doc.embedding)
                } for doc in file_embedding.document_embeddings]
            return []
