import os
import json
from domain.models import TestSuite
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import MessagesRole, Chat

class RequirementsAnalyzer:
    def __init__(self):
        load_dotenv()
        self._setup_gigachat()
        
    def _setup_gigachat(self):
        credentials = os.getenv('GIGACHAT_CREDENTIALS')
        
        if not credentials:
            raise ValueError("GigaChat API credentials missing")
        
        self.client = GigaChat(
            credentials=credentials,
            verify_ssl_certs=False
        )
        
    def _create_prompt(self, requirements: str) -> Chat:
        system_prompt = """Ты - генератор тест-кейсов. Твоя задача - анализ бизнес-требований и генерация тест-кейсов.
Следуй этим правилам для генерации тест-кейсов:
1. Идентифицируй и обогати пользовательские случаи из требований
2. Для каждого пользовательского случая создай несколько тест-кейсов, покрывающих различные сценарии
3. Каждый тест-кейс должен содержать детальные шаги и ожидаемые результаты
4. Включай и положительные и отрицательные тест-кейсы
5. Убедись, что генерируются уникальные идентификаторы пользовательских случаев (UC###) и тест-кейсов (TC###)
6. Каждый тест-кейс должен иметь ясные предусловия и ожидаемые результаты
7. Шаги должны быть атомарными и проверяемыми

Вывод должен быть валидным JSON-объектом с следующей структурой:
{
    "user_cases": [
        {
            "id": "UC###",
            "title": "User Case Title",
            "description": "Detailed description",
            "test_cases": [
                {
                    "id": "TC###",
                    "title": "Test Case Title",
                    "description": "What this test verifies",
                    "steps": [
                        {
                            "step_number": 1,
                            "description": "Step description",
                            "expected_result": "Expected result"
                        }
                    ],
                    "expected_outcome": "Overall outcome",
                    "user_case_id": "UC###"
                }
            ]
        }
    ]
}

ВАЖНО: Ваш ответ должен быть корректным объектом JSON, точно соответствующим этой структуре. Не включайте никакой дополнительный текст или пояснения за пределами структуры JSON."""

        messages = [
            {
                "role": MessagesRole.SYSTEM,
                "content": system_prompt
            },
            {
                "role": MessagesRole.USER,
                "content": f"Вот бизнес-требования для анализа:\n\n{requirements}"
            }
        ]
        return Chat(messages=messages)

    def analyze_requirements(self, content: str) -> TestSuite:
        try:
            chat = self._create_prompt(content)
            response = self.client.chat(chat)
            
            print("Ответ от GigaChat:")
            print(response.choices[0].message.content)
            print("\nAttempting to parse as JSON...")
            
            # Try to clean and parse the response
            response_text = response.choices[0].message.content.strip()
            
            # If the response starts with a backtick or code block marker, remove it
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            return TestSuite(**result)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")
            print("Response text was:")
            print(response_text)
            raise
        except Exception as e:
            print(f"Error: {str(e)}")
            raise
