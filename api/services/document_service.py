import tempfile
import os
from fastapi import UploadFile, HTTPException
from scripts.load_ba_document import BADocumentLoader
from scripts.load_sa_document import SADocumentLoader

class DocumentService:
    """Сервис для обработки загрузки документов"""
    
    def __init__(self):
        self.ba_loader = BADocumentLoader()
        self.sa_loader = SADocumentLoader()
    
    async def process_ba_document(self, file: UploadFile, confluence_link: str) -> dict:
        """Обработка BA документа"""
        return await self._process_document(file, confluence_link, self.ba_loader)
    
    async def process_sa_document(self, file: UploadFile, confluence_link: str) -> dict:
        """Обработка SA документа"""
        return await self._process_document(file, confluence_link, self.sa_loader)
    
    async def _process_document(self, file: UploadFile, confluence_link: str, loader) -> dict:
        """Общая логика обработки документа"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            try:
                loader.load_document(temp_file_path, confluence_link)
                return {
                    "status": "success",
                    "message": "Document uploaded and processed successfully"
                }
            finally:
                # Всегда удаляем временный файл
                os.unlink(temp_file_path)
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
