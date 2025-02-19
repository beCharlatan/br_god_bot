from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agents.evgeniy_agent.evgeniy_agent import EvgeniyAgent
from agents.conversation_manager import ConversationManager, State
from agents.nodes.rewrite_query import rewrite_query
from agents.nodes.grade_documents import grade_documents
from agents.nodes.classify_request import classify_request

# Initialize the graph and agents
graph_builder = StateGraph(State)
evgeniy = EvgeniyAgent()
conversation_manager = ConversationManager()

# Add nodes
graph_builder.add_node("evgeniy", evgeniy.invoke)
graph_builder.add_node("update_summary", conversation_manager.update_summary)
graph_builder.add_node("rewrite_query", rewrite_query)
graph_builder.add_node("grade_documents", grade_documents)
graph_builder.add_node("classify_request", classify_request)

# Add edges
graph_builder.add_edge(START, "classify_request")
graph_builder.add_edge("classify_request", "evgeniy")
graph_builder.add_edge("rewrite_query", "evgeniy")
graph_builder.add_edge("update_summary", END)

graph_builder.add_conditional_edges(
    "evgeniy",
    lambda state: state["request_type"],
    {
        "analyze": "grade_documents",
        "skip_analysis": "update_summary"
    }
)

# Add conditional edges from grade_documents
graph_builder.add_conditional_edges(
    "grade_documents",
    lambda state: state["routing_decision"],
    {
        "update_summary": "update_summary",
        "rewrite_query": "rewrite_query"
    }
)

# Create config for the graph
config = {
    "messages": [],
    "summary": None,
    "memory": {},
    "routing_decision": None,
    "request_type": None
}

# Compile the graph
graph = graph_builder.compile(checkpointer=MemorySaver())

# Set the initial state after compilation
graph.config = config