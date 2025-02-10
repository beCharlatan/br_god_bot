from typing import List, Dict
import numpy as np
from langchain_text_splitters import CharacterTextSplitter
from .gigachat_embeddings import GigaChatEmbeddings
from services.document_store import DocumentStore

class DocumentEmbedder:
    def __init__(self):
        self.store = DocumentStore()
        self.embeddings = GigaChatEmbeddings()
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=300,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False
        )
    
    def process_document(self, filename: str, content: str):
        # Split content into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Process each chunk
        for i, chunk in enumerate(chunks):
            chunk_name = f"{filename}_chunk_{i+1}"
            embedding = self.embeddings.create_embedding(chunk)
            self.store.store_document_embedding(chunk_name, chunk, embedding, filename)
        
    def find_similar_documents(self, query_text: str, limit: int = 5) -> List[Dict]:
        query_embedding = self.embeddings.create_embedding(query_text)
        
        return self.store.find_similar_documents(query_embedding, limit)
