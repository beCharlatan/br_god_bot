from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    """Модель для представления сообщения в чате"""
    role: MessageRole = Field(
        ...,
        description="Роль отправителя сообщения (user, assistant, или system)"
    )
    content: str = Field(
        ...,
        description="Текст сообщения",
        min_length=1
    )

class ChatRequest(BaseModel):
    """Модель для входящего запроса к чату"""
    message: str = Field(
        ...,
        description="Текст сообщения для отправки боту",
        min_length=1,
        examples=["Расскажи о функциональности продукта"]
    )
    thread_id: Optional[str] = Field(
        None,
        description="Идентификатор чата для сохранения контекста беседы",
        examples=["user_123"]
    )

class ChatResponse(BaseModel):
    """Модель для ответа от чата"""
    message: str = Field(
        ...,
        description="Ответ бота на сообщение пользователя"
    )
    thread_id: str = Field(
        ...,
        description="Идентификатор чата, использованный для ответа"
    )
    messages_history: List[ChatMessage] = Field(
        ...,
        description="История всех сообщений в данном чате"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "message": "Основная функциональность продукта включает...",
                "thread_id": "user_123",
                "messages_history": [
                    {"role": "user", "content": "Расскажи о функциональности продукта"},
                    {"role": "assistant", "content": "Основная функциональность продукта включает..."}
                ]
            }]
        }
    )
