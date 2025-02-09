from langchain.tools import tool
from typing import List, Dict, Any
from services.test_case_examples_service import TestCaseExamplesService


@tool
def get_good_test_case_examples(limit: int = 3) -> List[Dict[str, Any]]:
    """
    Получает примеры хороших тест-кейсов из базы данных для сравнения и обучения.
    
    Args:
        limit (int): Количество примеров для получения (по умолчанию 3)
        
    Returns:
        List[Dict]: Список хороших тест-кейсов с их метаданными
        
    Example:
        examples = get_good_test_case_examples(limit=2)
        # Возвращает 2 примера хороших тест-кейсов
    """
    return TestCaseExamplesService.get_good_examples(limit=limit)
