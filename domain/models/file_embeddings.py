from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import Base

class FileEmbeddings(Base):
    __tablename__ = 'file_embeddings'
    
    id = Column(Integer, primary_key=True)
    original_filename = Column(String(255), unique=True)
    
    # Relationship with DocumentImage
    images = relationship("DocumentImage", back_populates="file_embedding", cascade="all, delete-orphan")
