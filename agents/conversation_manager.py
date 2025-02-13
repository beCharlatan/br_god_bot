from typing import Dict, Any, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain.memory import ConversationSummaryMemory
from langchain_core.messages import HumanMessage
from services.llm.gigachat_service import GigaChatService


class State(TypedDict):
    messages: Annotated[list, add_messages]  # Conversation messages
    summary: Optional[str]  # Current conversation summary
    memory: Dict[str, Any]  # Memory state
    routing_decision: Optional[str]  # Routing decision from grade_documents node


class ConversationManager:
    def __init__(self):
        self.llm = GigaChatService().get_client()
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            max_token_limit=2000,
            memory_key="chat_history",
            return_messages=True
        )
    
    def update_summary(self, state: State) -> State:
        """Update the conversation summary based on new messages."""
        # Get the latest message
        if not state["messages"]:
            return state
            
        latest_message = state["messages"][-1]
        
        # Add the message to memory
        if isinstance(latest_message, HumanMessage):
            previous_message = state["messages"][-2].content if len(state["messages"]) > 1 else ""
            self.memory.save_context(
                {"input": latest_message.content},
                {"output": previous_message}
            )
        
        # Get the updated summary
        memory_variables = self.memory.load_memory_variables({})
        state["summary"] = str(memory_variables["chat_history"])
        
        # Store memory state
        state["memory"] = {
            "chat_history": memory_variables.get("chat_history", "")
        }
        
        return state
