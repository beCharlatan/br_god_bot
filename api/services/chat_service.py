from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agents.graph import graph
from api.models.chat import ChatMessage

class ChatService:
    """Сервис для обработки чат-сообщений"""
    
    def __init__(self):
        self.chat_histories: Dict[str, List[Any]] = {}
    
    def process_message(self, message: str, thread_id: str) -> tuple[str, List[ChatMessage]]:
        """Обработка входящего сообщения"""
        # Получаем или создаем историю сообщений для данного thread_id
        messages = self.chat_histories.get(thread_id, [])
        
        # Добавляем новое сообщение пользователя
        messages.append(HumanMessage(content=message))
        
        # Конфигурация для графа
        config = {"configurable": {"thread_id": thread_id}}
        
        # Вызываем граф для обработки сообщения
        state = graph.invoke({"messages": messages}, config)
        
        if not state or "messages" not in state:
            raise RuntimeError("Failed to process message")
            
        messages = state["messages"]
        self.chat_histories[thread_id] = messages
        
        # Получаем последнее сообщение от бота
        last_message = messages[-1]
        bot_response = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Преобразуем историю сообщений
        messages_history = self._convert_to_chat_messages(messages)
        
        return bot_response, messages_history
    
    def get_chat_history(self, thread_id: str) -> List[ChatMessage]:
        """Получение истории чата"""
        messages = self.chat_histories.get(thread_id, [])
        return self._convert_to_chat_messages(messages)
    
    def delete_chat_history(self, thread_id: str) -> None:
        """Удаление истории чата"""
        if thread_id in self.chat_histories:
            del self.chat_histories[thread_id]
    
    def _convert_to_chat_messages(self, messages: List[Any]) -> List[ChatMessage]:
        """Конвертация сообщений в формат API"""
        chat_messages = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else \
                   "system" if isinstance(msg, SystemMessage) else "assistant"
            content = msg.content if hasattr(msg, 'content') else str(msg)
            chat_messages.append(ChatMessage(role=role, content=content))
        return chat_messages
