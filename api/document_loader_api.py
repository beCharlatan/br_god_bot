from fastapi import UploadFile, Form
from .app import app
from .models.document import DocumentUploadResponse
from .services.document_service import DocumentService

# Инициализация сервиса
document_service = DocumentService()

from fastapi import status

@app.post(
    "/upload/ba-document",
    response_model=DocumentUploadResponse,
    tags=["documents"],
    summary="Загрузить BA документ",
    description="""Загружает и обрабатывает BA документ в формате .docx.
    
Процесс обработки:
* Загрузка документа
* Извлечение текста
* Создание векторных представлений
* Сохранение в базе данных
    """,
    status_code=status.HTTP_200_OK
)
async def upload_ba_document(
    file: UploadFile,
    confluence_link: str = Form(...)
) -> DocumentUploadResponse:
    return await document_service.process_ba_document(file, confluence_link)

@app.post(
    "/upload/sa-document",
    response_model=DocumentUploadResponse,
    tags=["documents"],
    summary="Загрузить SA документ",
    description="""Загружает и обрабатывает SA документ в формате .docx.
    
Процесс обработки:
* Загрузка документа
* Извлечение текста
* Создание векторных представлений
* Сохранение в базе данных
    """,
    status_code=status.HTTP_200_OK
)
async def upload_sa_document(
    file: UploadFile,
    confluence_link: str = Form(...)
) -> DocumentUploadResponse:
    return await document_service.process_sa_document(file, confluence_link)