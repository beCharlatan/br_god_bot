from typing import Dict
from domain.test_suite import TestSuite, UserCase, TestCase, TestStep
import json
import re


def generate_test_cases(content: str) -> Dict:
    """
    Извлекает и валидирует тест-кейсы из JSON-ответа.
    
    Args:
        content: Строка с JSON-ответом от модели
        
    Returns:
        Dict: Валидированные данные тест-кейсов
        
    Raises:
        ValueError: Если данные не соответствуют ожидаемому формату
    """
    # Find JSON part in the response using regex
    json_match = re.search(r'\{[\s\S]*\}', content)
    if not json_match:
        raise ValueError("JSON не найден в ответе")
        
    json_str = json_match.group(0)
    json_data = json.loads(json_str)
    
    # Validate using Pydantic models
    test_suite = TestSuite(
        user_cases=[
            UserCase(
                id=uc['id'],
                title=uc['title'],
                description=uc['description'],
                test_cases=[
                    TestCase(
                        id=tc['id'],
                        title=tc['title'],
                        description=tc['description'],
                        steps=[
                            TestStep(
                                step_number=step['step_number'],
                                description=step['description'],
                                expected_result=step['expected_result']
                            ) for step in tc['steps']
                        ],
                        expected_outcome=tc['expected_outcome'],
                        user_case_id=tc['user_case_id']
                    ) for tc in uc['test_cases']
                ]
            ) for uc in json_data['user_cases']
        ]
    )
    
    return test_suite
