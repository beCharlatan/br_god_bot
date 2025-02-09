from langchain.tools import tool
from typing import List, Dict, Any
from services.test_case_examples_service import TestCaseExamplesService


@tool
def get_bad_test_case_examples(limit: int = 3) -> List[Dict[str, Any]]:
    """
    Получает примеры плохих тест-кейсов из базы данных для анализа и сравнения.
    
    Args:
        limit (int): Количество примеров для получения (по умолчанию 3)
        
    Returns:
        List[Dict]: Список плохих тест-кейсов с их метаданными
        
    Example:
        examples = get_bad_test_case_examples(limit=2)
        # Возвращает 2 примера плохих тест-кейсов для анализа
    """
    return TestCaseExamplesService.get_bad_examples(limit=limit)
