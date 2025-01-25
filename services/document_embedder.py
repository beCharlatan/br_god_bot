from typing import List, Dict
import numpy as np
from langchain_text_splitters import CharacterTextSplitter
from config.database import db
from domain.models.document_embedding import DocumentEmbedding
from .gigachat_embeddings import GigaChatEmbeddings

class DocumentEmbedder:
    def __init__(self):
        db.create_tables()
        self.embeddings = GigaChatEmbeddings()
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False
        )
    
    def store_embedding(self, filename: str, content: str, embedding: List[float]):
        with next(db.get_db()) as session:
            doc_embedding = DocumentEmbedding(
                filename=filename,
                content=content,
                embedding=str(embedding)
            )
            session.add(doc_embedding)
            session.commit()
    
    def process_document(self, filename: str, content: str):
        # Split content into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            chunk_name = f"{filename}_chunk_{i+1}"
            embedding = self.embeddings.create_embedding(chunk)
            self.store_embedding(chunk_name, chunk, embedding)
        
    def find_similar_documents(self, query_text: str, limit: int = 5) -> List[Dict]:
        query_embedding = self.embeddings.create_embedding(query_text)
        
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
