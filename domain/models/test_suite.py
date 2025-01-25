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
    user_cases: List[UserCase] = Field(
        description="Список пользовательских случаев использования и их тест-кейсов"
    )
