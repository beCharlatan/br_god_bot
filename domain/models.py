from typing import List
from pydantic.v1 import BaseModel, Field

class TestStep(BaseModel):
    step_number: int = Field(description="Sequential number of the test step")
    description: str = Field(description="Description of what should be done in this step")
    expected_result: str = Field(description="Expected result after performing this step")

class TestCase(BaseModel):
    id: str = Field(description="Unique identifier for the test case (format: TC###)")
    title: str = Field(description="Brief title describing the test case")
    description: str = Field(description="Detailed description of what this test case verifies")
    steps: List[TestStep] = Field(description="Ordered list of steps to execute the test")
    expected_outcome: str = Field(description="Overall expected outcome of the test case")
    user_case_id: str = Field(description="ID of the user case this test belongs to")

class UserCase(BaseModel):
    id: str = Field(description="Unique identifier for the user case (format: UC###)")
    title: str = Field(description="Brief title describing the user case")
    description: str = Field(description="Detailed description of the user case")
    test_cases: List[TestCase] = Field(description="List of test cases for this user case")

class TestSuite(BaseModel):
    user_cases: List[UserCase] = Field(description="List of user cases with their test cases")
