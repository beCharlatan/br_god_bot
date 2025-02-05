from typing import List, Dict, Any, Union
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from domain.test_suite import TestSuite
from services.gigachat_service import GigaChatService
from services.document_store import DocumentStore
from .tools.get_document_content import get_document_content
import json

class VolodyaAgent:
    def __init__(self):
        self.system_prompt = """
        Ты — опытный тестировщик продукта. Твоя основная задача - формирование тестовых кейсов, 
        которые позволят проверить работу продукта на полноценном уровне.
        Для формирования тестовых кейсов ты должен использовать базу знаний и бизнесовые требования продукта.
        Для того, что сформировать тестовые кейсы, ты должен узнать у пользователя по каким бизнесовым требованиям формировать тестовые кейсы.
        """
        self.document_store = DocumentStore()
        self.tools = [get_document_content]
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
    
    def _parse_json_response(self, text: str) -> Union[Dict, None]:
        """Try to extract and parse JSON from the response text.

        Args:
            text: Response text that might contain JSON

        Returns:
            Dict if JSON found and parsed, None otherwise
        """
        try:
            # Find JSON-like structure in the text
            start = text.find('{')
            end = text.rfind('}')
            if start != -1 and end != -1:
                json_str = text[start:end + 1]
                return json.loads(json_str)
            return None
        except json.JSONDecodeError:
            return None

    def _create_test_suite(self, data: Dict) -> Union[TestSuite, None]:
        """Create TestSuite object from parsed JSON data.

        Args:
            data: Dictionary containing test suite data

        Returns:
            TestSuite object if valid, None otherwise
        """
        try:
            return TestSuite.parse_obj(data)
        except Exception:
            return None

    def invoke(self, messages: List[AnyMessage], config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user messages and provide answers based on the knowledge base.
        
        Args:
            messages: List of conversation messages
            config: Optional configuration parameters
            
        Returns:
            Dict containing the agent's response with potentially parsed TestSuite
        """
        if config is None:
            config = {"configurable": {"thread_id": 'VolodyaAgent'}}

        response = self.agent.invoke({"messages": messages}, config=config)
        
        # Try to parse the last message as JSON
        if isinstance(response["messages"][-1], AIMessage):
            json_data = self._parse_json_response(response['output'].content)
            if json_data:
                test_suite = self._create_test_suite(json_data)
                if test_suite:
                    response['test_suite'] = test_suite
        
        return response
