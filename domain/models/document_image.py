from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class DocumentImage(Base):
    __tablename__ = 'document_images'
    
    id = Column(Integer, primary_key=True)
    image_name = Column(String(255), nullable=False)     # Original image name from doc
    minio_path = Column(String(255), nullable=False)     # MinIO object path
    file_embedding_id = Column(Integer, ForeignKey('file_embeddings.id', ondelete='CASCADE'))

    # Relationship with FileEmbeddings
    file_embedding = relationship("FileEmbeddings", back_populates="images")

