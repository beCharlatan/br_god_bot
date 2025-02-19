from pydantic import BaseModel, Field, ConfigDict
from fastapi import UploadFile, Form
from enum import Enum

class DocumentStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class DocumentUploadRequest(BaseModel):
    """Базовая модель для загрузки документа"""
    file: UploadFile = Field(
        ...,
        description="Файл документа в формате .docx"
    )
    confluence_link: str = Field(
        ...,
        description="Ссылка на документ в Confluence",
        examples=["https://confluence.example.com/pages/123"]
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Разрешаем использование UploadFile
        json_schema_extra={
            "examples": [{
                "file": "document.docx",
                "confluence_link": "https://confluence.example.com/pages/123"
            }]
        }
    )

class DocumentUploadResponse(BaseModel):
    """Модель ответа на загрузку документа"""
    status: DocumentStatus = Field(
        ...,
        description="Статус загрузки документа (success или error)"
    )
    message: str = Field(
        ...,
        description="Сообщение о результате загрузки"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "status": "success",
                "message": "Document uploaded and processed successfully"
            }]
        }
    )
