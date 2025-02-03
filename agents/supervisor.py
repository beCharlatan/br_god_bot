from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, END, StateGraph, START
from .evgeniy_agent.evgeniy_agent import EvgeniyAgent
from .upload_agent.upload_agent import UploadAgent
from services.gigachat_service import GigaChatService
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["evgeniy", "upload", "FINISH"]

class State(MessagesState):
    next: str

class Supervisor:
    def __init__(self):
        self.members = ["evgeniy", "upload"]
        self.options = self.members + ["FINISH"]
        self.system_prompt = (
            f"Ты супервизор и твоя задача перенаправлять запросы пользователя к одному из агентов: {self.members}."
            "Когда все агенты завершат свою работу, ответь FINISH. Если ты получишь сообщение от агента, ответь FINISH."
        )
        self.llm = GigaChatService().get_client()
        self.evgeniy_agent = EvgeniyAgent()
        self.upload_agent = UploadAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(State)
        builder.add_node("supervisor", self.supervisor_node)
        builder.add_node("evgeniy", self.evgeniy_node)
        builder.add_node("upload", self.upload_node)
        builder.add_edge(START, "supervisor")
        return builder.compile(checkpointer=MemorySaver())

    def supervisor_node(self, state: State) -> Command[Literal["supervisor", "evgeniy", "upload", END]]:
        if isinstance(state["messages"][-1], AIMessage):
            return Command(goto=END, update={"next": END})
        
        messages = [HumanMessage(content=self.system_prompt, name="system")] + state["messages"]
        response = self.llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    def evgeniy_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.evgeniy_agent.invoke(state["messages"])
        return Command(
            update={"messages": result["messages"]},
            goto="supervisor",
        )

    def upload_node(self, state: State) -> Command[Literal["supervisor"]]:
        result = self.upload_agent.invoke(state["messages"])
        return Command(
            update={"messages": result["messages"]},
            goto="supervisor",
        )

    def invoke(self, state: State, config: dict) -> State:
        return self.graph.invoke(state, config=config)