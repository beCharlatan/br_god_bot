from typing import List
from pydantic.v1 import BaseModel, Field


class TestStep(BaseModel):
    step_number: int = Field(
        description="Порядковый номер этапа тестирования"
    )
    description: str = Field(
        description="Описание этапа тестирования"
    )
    expected_result: str = Field(
        description="Ожидаемый результат этапа тестирования"
    )


class TestCase(BaseModel):
    id: str = Field(
        description="Уникальный идентификатор тест-кейса (формат: TC###)"
    )
    title: str = Field(
        description="Короткое описание тест-кейса"
    )
    description: str = Field(
        description="Детальное описание того, что проверяет этот тест-кейс"
    )
    steps: List[TestStep] = Field(
        description="Последовательность шагов, которые необходимо выполнить для выполнения тест-кейса"
    )
    expected_outcome: str = Field(
        description="Ожидаемый результат тест-кейса"
    )
    user_case_id: str = Field(
        description="ID пользователя, к которому относится этот тест-кейс"
    )


class UserCase(BaseModel):
    id: str = Field(
        description="Уникальный идентификатор для обращения к пользователю (формат: UC###)"
    )
    title: str = Field(
        description="Краткое название, описывающее пользовательский кейс"
    )
    description: str = Field(
        description="Детальное описание того, что проверяет этот тест-кейс"
    )
    test_cases: List[TestCase] = Field(
        description="Список тест-кейсов для этого пользователя"
    )


class TestSuite(BaseModel):
    """Структура для хранения и организации тестовых кейсов и пользовательских сценариев.

    Этот класс представляет собой корневую структуру для всех тестовых артефактов.
    Он содержит список пользовательских случаев (UserCase), каждый из которых включает
    набор тест-кейсов (TestCase) с детальными шагами тестирования (TestStep).

    Формат данных:
    - Все ID пользовательских случаев должны быть в формате UC### (где ### - порядковый номер)
    - Все ID тест-кейсов должны быть в формате TC### (где ### - порядковый номер)
    - Каждый тест-кейс должен содержать минимум 2 шага
    - Все описания должны быть на русском языке
    """
    user_cases: List[UserCase] = Field(
        description="Список пользовательских случаев использования и их тест-кейсов"
    )
