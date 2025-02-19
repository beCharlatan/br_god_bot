from langchain_core.messages import HumanMessage
from services.llm.gigachat_service import GigaChatService
from agents.conversation_manager import State
from langchain_core.messages import HumanMessage
from services.llm.gigachat_service import GigaChatService
from agents.conversation_manager import State

def rewrite_query(state: State) -> State:
    """
    Transform the query to produce a better question.

    Args:
        state: The current state containing messages and other data

    Returns:
        State: The modified state with the rewritten query
    """
    print("---TRANSFORM QUERY---")
    messages = state["messages"]
    question = messages[0].content

    msg = [
        HumanMessage(
            content=f""" \n 
    Проанализируй исходный запрос и определи его скрытый смысл или намерение. \n
    Исходный вопрос:
    \n ------- \n
    {question} 
    \n ------- \n
    Сформулируйте улучшенный вопрос: """,
        )
    ]

    # Get response from model
    model = GigaChatService().get_client()
    response = model.invoke(msg)

    # Update state in place
    state["messages"] = [response]
    state["routing_decision"] = None  # Reset routing decision as we're starting a new iteration
    
    # Return modified state
    return state