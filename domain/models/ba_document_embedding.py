from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class BADocumentEmbedding(Base):
    __tablename__ = 'ba_document_embeddings'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Text)
    document_meta_id = Column(Integer, ForeignKey('documents_meta.id'))
    
    # Relationship back to document metadata
    document_meta = relationship('DocumentMeta', back_populates='ba_embeddings')