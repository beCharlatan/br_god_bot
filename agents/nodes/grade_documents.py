from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from services.llm.gigachat_service import GigaChatService
from agents.conversation_manager import State   


def grade_documents(state: State) -> State:
    """
    Determines whether the retrieved documents are relevant to the question.

    Args:
        state: The current state containing messages and other data

    Returns:
        State: The modified state with grading decision
    """
    print("---CHECK RELEVANCE---")

    # Data model
    class grade(BaseModel):
        """Binary score for relevance check."""
        binary_score: str = Field(description="Relevance score 'yes' or 'no'")

    # LLM
    model = GigaChatService().get_client()

    # LLM with tool and validation
    llm_with_tool = model.with_structured_output(grade)

    # Prompt
    prompt = PromptTemplate(
        template="Ты — опытный аналитик, оценивающий релевантность документов для ответа на вопрос.\n"
        "## Вопрос\n"
        "{question}\n"
        "## Документы\n"
        "{context}\n\n"
        "Твоя задача — оценить, насколько приведенные документы релевантны для ответа на вопрос. "
        "Учитывай полноту информации, актуальность данных и соответствие тематике.\n"
        "Если документ содержит ключевое слово или семантическое значение, связанное с вопросом пользователя, "
        "оцените его как релевантный. \n"
        "Дайте бинарный ответ 'yes' или 'no', чтобы указать, является ли документ релевантным для вопроса.",
        input_variables=["question", "context"],
    )

    # Chain
    chain = prompt | llm_with_tool

    messages = state["messages"]
    last_message = messages[-1]

    question = messages[0].content
    docs = last_message.content

    scored_result = chain.invoke({"question": question, "context": docs})
    score = scored_result.binary_score

    # Add decision to state
    state["routing_decision"] = "update_summary" if score == "yes" else "rewrite_query"

    if score == "yes":
        print("---DECISION: DOCS RELEVANT---")
    else:
        print("---DECISION: DOCS NOT RELEVANT---")
        print(score)

    return state