import json
from domain.models import TestSuite
from gigachat.models import MessagesRole, Chat
from .gigachat_service import GigaChatService

class RequirementsAnalyzer:
    def __init__(self):
        self.client = GigaChatService().get_client()
        
    def _create_prompt(self, requirements: str) -> Chat:
        system_prompt = """Ты - генератор тест-кейсов. Твоя задача - анализ бизнес-требований и генерация тест-кейсов.
Следуй этим правилам для генерации тест-кейсов:
1. Идентифицируй и обогати пользовательские случаи из требований
2. Для каждого пользовательского случая создай несколько тест-кейсов, покрывающих различные сценарии
3. Каждый тест-кейс должен содержать детальные шаги и ожидаемые результаты
4. Включай и положительные и отрицательные тест-кейсы
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
                    "expected_outcome": "Overall expected outcome",
                    "user_case_id": "UC###"
                }
            ]
        }
    ]
}"""

        return Chat(
            messages=[
                {"role": MessagesRole.SYSTEM, "content": system_prompt},
                {"role": MessagesRole.USER, "content": requirements}
            ]
        )
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from potentially markdown-wrapped text."""
        # If the response is wrapped in markdown code block
        if text.startswith("```"):
            # Find the first and last code block markers
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return text[start:end]
        return text
    
    def analyze_requirements(self, content: str) -> TestSuite:
        prompt = self._create_prompt(content)
        
        response = self.client.chat(prompt)
        response_text = response.choices[0].message.content
        
        print("\nGigaChat Response:")
        print("=" * 80)
        print(response_text)
        print("=" * 80)
        
        try:
            json_text = self._extract_json(response_text)
            test_data = json.loads(json_text)
            return TestSuite(**test_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse GigaChat response as JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to create TestSuite from response: {str(e)}")
