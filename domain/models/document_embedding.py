from sqlalchemy import Column, Integer, String, Text
from config.database import Base

class DocumentEmbedding(Base):
    __tablename__ = 'document_embeddings'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    content = Column(Text)
    embedding = Column(Text)
