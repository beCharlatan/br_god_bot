from sqlalchemy import Column, Integer, String
from config.database import Base

class FileEmbeddings(Base):
    __tablename__ = 'file_embeddings'
    
    id = Column(Integer, primary_key=True)
    original_filename = Column(String(255), unique=True)
