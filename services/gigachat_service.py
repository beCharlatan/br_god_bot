import os
from gigachat import GigaChat

class GigaChatService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GigaChatService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        credentials = os.getenv('GIGACHAT_CREDENTIALS')
        
        if not credentials:
            raise ValueError("GigaChat API credentials missing")
        
        self.client = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False
        )
    
    def get_client(self) -> GigaChat:
        return self.client
