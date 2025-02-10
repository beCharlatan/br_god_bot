from typing import List, Dict, Any
from langchain_core.messages import AnyMessage
from services.gigachat_service import GigaChatService
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from .tools.process_document import process_document

class UploadAgent:
    """Agent responsible for parsing documents and uploading them to the knowledge base."""
    
    def __init__(self):
        self.system_prompt = """Ты - агент, который должен парсить документы и загружать их в единую базу знаний.
        Твоя главная задача - парсинг документа, разбивка на эмбединги и загрузка эмбедингов в базу данных.
        
        Важно: Перед обработкой документа тебе нужно получить следующую информацию от пользователя:
        1. Путь до файла для загрузки
        
        После получения пути к файлу, используй инструмент process_document для его обработки.
        Используй инструмент human_assistance для запроса любой дополнительной информации.
        
        Если возникают ошибки или нужна дополнительная информация - не стесняйся спрашивать у пользователя.
        """
        self.tools = [process_document]
        self.model = GigaChatService().get_client()
        self.agent = self._create_agent()
        
    def _create_agent(self):
        """Create and configure the React agent."""
        return create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=MemorySaver(),
            state_modifier=self.system_prompt
        )
        
    def invoke(self, messages: List[AnyMessage], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user messages and handle document uploads.
        
        Args:
            messages: List of conversation messages
            config: Optional configuration parameters
            
        Returns:
            Dict containing the agent's response
        """
        if config is None:
            config = {"configurable": {"thread_id": 'UploadAgent'}}
    
        return self.agent.invoke({"messages": messages}, config=config)
