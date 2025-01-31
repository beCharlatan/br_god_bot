from sqlalchemy import Column, Integer, String, Text, ForeignKey
from config.database import Base

class DocumentEmbedding(Base):
    __tablename__ = 'document_embeddings'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    content = Column(Text)
    embedding = Column(Text)
    file_embedding_id = Column(Integer, ForeignKey('file_embeddings.id'))
