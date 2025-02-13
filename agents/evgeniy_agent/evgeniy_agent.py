from typing import List, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.llm.gigachat_service import GigaChatService
from .tools.find_related_ba_documents import find_related_ba_documents
from .tools.find_related_sa_documents import find_related_sa_documents
from .tools.get_documents_names import get_documents_names

class EvgeniyAgent:    
    def __init__(self):
        self.system_prompt = """
        Вы - специализированный ассистент по работе с базой знаний продукта. Ваши основные принципы:

        1. ТОЧНОСТЬ:
        - Отвечайте только на основе имеющейся информации в базе знаний
        - Всегда приводите точные цитаты из документации
        - Если информации недостаточно или её нет, прямо сообщите об этом

        2. СТРУКТУРА ОТВЕТА:
        - Начинайте с прямого ответа на вопрос
        - Подкрепляйте ответ релевантными цитатами из базы знаний
        - Указывайте источник каждой цитаты

        3. ОГРАНИЧЕНИЯ:
        - Никогда не додумывайте информацию
        - Не давайте предположений или интерпретаций
        - При неполной информации запрашивайте уточнения

        4. ФОРМАТ ЦИТИРОВАНИЯ:
        ```
        Источник: [название_документа]
        "точная цитата из документа"
        ```

        Используйте доступные инструменты для поиска информации в базе знаний.
        """

        self.tools = [find_related_ba_documents, find_related_sa_documents, get_documents_names]
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
    
    def invoke(self, state: Dict[str, List[AnyMessage]], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user messages and provide answers based on the knowledge base.
        
        Args:
            state: Dictionary containing messages list and conversation summary
            config: Optional configuration parameters
            
        Returns:
            Dict containing the agent's response
        """
        if config is None:
            config = {"configurable": {"thread_id": 'EvgeniyAgent'}}

        # Add conversation summary to the system prompt if available
        current_prompt = self.system_prompt
        if state.get("summary"):
            current_prompt += """

Контекст предыдущей беседы:
{}

Используйте этот контекст для более точных и контекстно-зависимых ответов.""".format(state["summary"])
            
        # Update the agent with the current prompt
        self.agent = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=MemorySaver(),
            state_modifier=current_prompt
        )
            
        # Get response from agent
        response = self.agent.invoke(state, config=config)
        
        # Preserve routing_decision field if it exists
        if "routing_decision" in state:
            response["routing_decision"] = state["routing_decision"]
        else:
            response["routing_decision"] = None
            
        return response
