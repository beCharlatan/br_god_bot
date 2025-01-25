from typing import List
import os
from langchain_gigachat.embeddings import GigaChatEmbeddings as LangchainGigaChatEmbeddings

class GigaChatEmbeddings:
    def __init__(self):
        credentials = os.getenv('GIGACHAT_CREDENTIALS')
        if not credentials:
            raise ValueError("GigaChat API credentials missing")
            
        self.embeddings = LangchainGigaChatEmbeddings(
            credentials=credentials,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False
        )
    
    def create_embedding(self, text: str) -> List[float]:
        result = self.embeddings.embed_query(text)
        return result
