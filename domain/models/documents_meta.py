from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class DocumentMeta(Base):
    __tablename__ = 'documents_meta'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    ba_document_confluence_link = Column(String(255))
    sa_document_confluence_link = Column(String(255))
    
    # Relationships
    ba_embeddings = relationship('BADocumentEmbedding', back_populates='document_meta')
    sa_embeddings = relationship('SADocumentEmbedding', back_populates='document_meta')