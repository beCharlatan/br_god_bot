from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agents.evgeniy_agent.evgeniy_agent import EvgeniyAgent
from agents.conversation_manager import ConversationManager, State


# Initialize the graph and agents
graph_builder = StateGraph(State)
evgeniy = EvgeniyAgent()
conversation_manager = ConversationManager()

# Add nodes
graph_builder.add_node("evgeniy", evgeniy.invoke)
graph_builder.add_node("update_summary", conversation_manager.update_summary)

# Add edges
graph_builder.add_edge(START, "evgeniy")
graph_builder.add_edge("evgeniy", "update_summary")
graph_builder.add_edge("update_summary", END)

# Create config for the graph
config = {
    "messages": [],
    "summary": None,
    "memory": {}
}

# Compile the graph
graph = graph_builder.compile(checkpointer=MemorySaver())

# Set the initial state after compilation
graph.config = config