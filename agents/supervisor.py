from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, END, StateGraph, START
from .evgeniy_agent.evgeniy_agent import EvgeniyAgent
from .upload_agent.upload_agent import UploadAgent
from services.gigachat_service import GigaChatService
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

members = ["evgeniy", "upload"]
options = members + ["FINISH"]

system_prompt = (
    f"Ты супервизор и твоя задача перенаправлять запросы пользователя к одному из агентов: {members}."
    "Когда все агенты завершат свою работу, ответь FINISH. Если ты получишь сообщение от агента, ответь FINISH."
)

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*options]

llm = GigaChatService().get_client()

class State(MessagesState):
    next: str

def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
    if isinstance(state["messages"][-1], AIMessage):
        return Command(goto=END, update={"next": END})
    
    messages = [HumanMessage(content=system_prompt, name="system")] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})

def evgeniy_node(state: State) -> Command[Literal["supervisor"]]:
    result = evgeniy_agent.invoke(state["messages"])
    return Command(
        update={"messages": result["messages"]},
        goto="supervisor",
    )

def upload_node(state: State) -> Command[Literal["supervisor"]]:
    result = upload_agent.invoke(state["messages"])
    return Command(
        update={"messages": result["messages"]},
        goto="supervisor",
    )

# Initialize agents
evgeniy_agent = EvgeniyAgent()
upload_agent = UploadAgent()

# Build the graph
builder = StateGraph(State)
builder.add_node("supervisor", supervisor_node)
builder.add_node("evgeniy", evgeniy_node)
builder.add_node("upload", upload_node)
builder.add_edge(START, "supervisor")
graph = builder.compile(checkpointer=MemorySaver())