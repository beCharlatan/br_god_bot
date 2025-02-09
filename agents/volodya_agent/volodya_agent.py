from typing import List, Dict, Any
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from services.gigachat_service import GigaChatService
from services.document_store import DocumentStore
from services.test_suite_service import TestSuiteService
from .tools.get_document_content import get_document_content
from .tools.generate_test_cases import generate_test_cases
from .tools.get_good_test_case_examples import get_good_test_case_examples
from .tools.get_bad_test_case_examples import get_bad_test_case_examples

class VolodyaAgent:
    def __init__(self):
        self.system_prompt = """
        Ты — опытный тестировщик продукта. Твоя основная задача - формирование тестовых кейсов, 
        которые позволят проверить работу продукта на полноценном уровне.
        
        Для формирования тестовых кейсов ты должен:
        1. Использовать базу знаний и бизнес-требования
        2. Анализировать примеры хороших и плохих тест-кейсов
        3. Следовать лучшим практикам тестирования
        
        У тебя есть доступ к следующим инструментам:
        - get_document_content: получить содержимое документа
        - generate_test_cases: сгенерировать тест-кейсы
        - get_good_test_case_examples: получить примеры хороших тест-кейсов
        - get_bad_test_case_examples: получить примеры плохих тест-кейсов для анализа
        
        При создании тест-кейсов:
        1. Изучи примеры хороших тест-кейсов для понимания формата
        2. Проанализируй плохие примеры, чтобы избежать их недостатков
        3. Следуй структуре и формату из хороших примеров
        
        ВАЖНО: Твой ответ всегда должен быть в формате JSON со следующей структурой:
        {
            "user_cases": [
                {
                    "id": "UC001",  // Формат: UC### где ### - порядковый номер
                    "title": "Название пользовательского кейса",
                    "description": "Детальное описание пользовательского кейса",
                    "test_cases": [
                        {
                            "id": "TC001",  // Формат: TC### где ### - порядковый номер
                            "title": "Название тест-кейса",
                            "description": "Детальное описание тест-кейса",
                            "steps": [
                                {
                                    "step_number": 1,
                                    "description": "Описание шага",
                                    "expected_result": "Ожидаемый результат"
                                }
                            ],
                            "expected_outcome": "Общий ожидаемый результат тест-кейса",
                            "user_case_id": "UC001"  // ID родительского пользовательского кейса
                        }
                    ]
                }
            ]
        }
        
        Все описания должны быть на русском языке.
        Каждый тест-кейс должен содержать минимум 2 шага.
        """

        self.document_store = DocumentStore()
        self.tools = [get_document_content, generate_test_cases, get_good_test_case_examples, get_bad_test_case_examples]
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
            Dict containing the agent's response with potentially parsed TestSuite
        """
        if config is None:
            config = {"configurable": {"thread_id": 'VolodyaAgent'}}

        response = self.agent.invoke({"messages": messages}, config=config)

        if isinstance(response['messages'][-1], AIMessage):
            try:
                # Generate and validate test cases
                content = response['messages'][-1].content
                test_data = generate_test_cases(content)
                
                # Save to database
                db_test_suite, stats = TestSuiteService.save_test_suite(test_data)
                
                # Add success message
                response['messages'].append(AIMessage(
                    content=f"Тест-кейсы успешно сгенерированы и сохранены в базу данных:\n" + 
                            f"- Создан тест-сьют (ID: {db_test_suite.id})\n" + 
                            f"- Добавлено пользовательских кейсов: {stats['user_cases_count']}\n" + 
                            f"- Общее количество тест-кейсов: {stats['test_cases_count']}\n"
                ))
                
                response['test_suite'] = test_data
                
            except Exception as e:
                error_msg = f"Ошибка при сохранении тест-кейсов: {str(e)}"
                print(error_msg)
                response['messages'].append(AIMessage(content=error_msg))
        
        return response
