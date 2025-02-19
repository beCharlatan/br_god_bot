from agents.conversation_manager import State   

def classify_request(state: State) -> State:
    """
    Classifies the user's request to determine if it requires relevance analysis.
    Returns 'analyze' if the request is a question or requires explanation,
    'skip_analysis' otherwise.
    """
    last_message = state["messages"][-1]
    if not isinstance(last_message, dict) or "content" not in last_message:
        return {"request_type": "skip_analysis"}
    
    content = last_message["content"].lower()
    
    # Keywords indicating a question or request for explanation
    question_indicators = [
        "?", "что", "как", "почему", "когда", "где", "кто", "какой", "какая", "какие",
        "объясни", "расскажи", "помоги понять", "можешь описать",
        "покажи", "дай", "нужно знать", "хочу знать",
        "мог бы ты", "не мог бы ты", "пожалуйста объясни", "подскажи",
        "зачем", "куда", "откуда", "чей", "чья", "чьё", "чьи"
    ]
    
    # Check if the message contains any question indicators
    needs_analysis = any(indicator in content for indicator in question_indicators)

    state["request_type"] = "analyze" if needs_analysis else "skip_analysis"

    return state
