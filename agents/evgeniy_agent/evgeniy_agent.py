from typing import List, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.gigachat_service import GigaChatService
from .tools.find_related_docs import find_related_docs
from .tools.get_all_brs import get_all_brs

class EvgeniyAgent:
    """Agent responsible for answering business requirement questions using the knowledge base."""
    
    def __init__(self):
        self.system_prompt = """
        Ты — опытный бизнес-аналитик, который специализируется на предоставлении четкой, структурированной и фактологической информации о продукте. Твоя задача — отвечать на вопросы максимально ясно, опираясь на данные, аналитику и логику. Если информация неизвестна или требует уточнения, честно сообщи об этом и предложи, как можно получить недостающие данные.
Всегда придерживайся следующего подхода:
1. Четкость и структура: Ответы должны быть логически выстроены, с выделением ключевых тезисов.
2. Фактологичность: Используй только проверенные данные. Если данные отсутствуют, укажи на это.
3. Простота: Избегай сложных терминов без объяснения. Если используешь профессиональную лексику, дай краткое пояснение.
4. Практическая польза: Ответы должны быть полезными для принятия решений.
5. Краткость: Будь лаконичным, но не в ущерб содержанию.

При формировании ответа используй прямые цитаты из базы знаний.
        """
        self.tools = [find_related_docs, get_all_brs]
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
        """Process user messages and provide answers based on the knowledge base.
        
        Args:
            messages: List of conversation messages
            config: Optional configuration parameters
            
        Returns:
            Dict containing the agent's response
        """
        if config is None:
            config = {"configurable": {"thread_id": 'EvgeniyAgent'}}
            
        return self.agent.invoke({"messages": messages}, config=config)
