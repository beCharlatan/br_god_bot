from fastapi import HTTPException
from .app import app
from .models.chat import ChatRequest, ChatResponse
from .services.chat_service import ChatService

# Инициализация сервиса
chat_service = ChatService()

from fastapi import status

@app.post(
    "/chat",
    response_model=ChatResponse,
    tags=["chat"],
    summary="Отправить сообщение боту",
    description="""Отправляет сообщение боту и получает ответ.
    
Поддерживает:
* Сохранение истории сообщений по thread_id
* Контекстные ответы на основе предыдущих сообщений
    """,
    status_code=status.HTTP_200_OK
)
async def chat(request: ChatRequest):
    try:
        thread_id = request.thread_id or "default"
        bot_response, messages_history = chat_service.process_message(request.message, thread_id)
        
        return ChatResponse(
            message=bot_response,
            thread_id=thread_id,
            messages_history=messages_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(
    "/chat/{thread_id}/history",
    tags=["chat"],
    summary="Получить историю чата",
    description="Возвращает историю сообщений для указанного thread_id",
    status_code=status.HTTP_200_OK
)
async def get_chat_history(thread_id: str):
    try:
        return chat_service.get_chat_history(thread_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete(
    "/chat/{thread_id}",
    tags=["chat"],
    summary="Удалить историю чата",
    description="Удаляет всю историю сообщений для указанного thread_id",
    status_code=status.HTTP_200_OK
)
async def delete_chat_history(thread_id: str):
    try:
        chat_service.delete_chat_history(thread_id)
        return {"status": "success", "message": f"Chat history for thread {thread_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
