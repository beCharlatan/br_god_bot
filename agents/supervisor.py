from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState, END, StateGraph, START
from .evgeniy_agent.evgeniy_agent import EvgeniyAgent
from .upload_agent.upload_agent import UploadAgent
from .volodya_agent.volodya_agent import VolodyaAgent
from services.gigachat_service import GigaChatService
from langchain_core.messages import AIMessage, SystemMessage
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal["evgeniy", "upload", "volodya", "FINISH"]

class State(MessagesState):
    next: str

class Supervisor:
    def __init__(self):
        self.evgeniy_agent = EvgeniyAgent()
        self.upload_agent = UploadAgent()
        self.volodya_agent = VolodyaAgent()
        self.members = ["evgeniy", "upload", "volodya"]
        self.options = self.members + ["FINISH"]
        
        # Create prompt for the supervisor
        self.system_prompt = (
            "You are a team manager responsible for routing user requests to appropriate agents. "
            "Analyze the request and conversation history to select the most appropriate agent."
            "\n\nAvailable agents:\n"
            f"1. Evgeniy - {self.evgeniy_agent.system_prompt}\n"
            f"2. Upload - {self.upload_agent.system_prompt}\n"
            f"3. Volodya - {self.volodya_agent.system_prompt}\n"
            "\nWhen all work is complete or when receiving a message from an agent, return FINISH."
            f"Return on of {self.options}"
        )
        
        self.llm = GigaChatService().get_client()
        self.graph = self._build_graph()

    def _build_graph(self):
        builder = StateGraph(State)
        builder.add_node("supervisor", self.supervisor_node)
        builder.add_node("evgeniy", self.evgeniy_node)
        builder.add_node("upload", self.upload_node)
        builder.add_node("volodya", self.volodya_node)
        builder.add_edge(START, "supervisor")
        return builder.compile(checkpointer=MemorySaver())

    def supervisor_node(self, state: State) -> Command[Literal["supervisor", "evgeniy", "upload", "volodya"]]:
        if isinstance(state["messages"][-1], AIMessage):
            return Command(goto=END, update={"next": END})
        
        # Get last 5 messages for context
        chat_history = state["messages"][-5:] if len(state["messages"]) > 5 else state["messages"]
        
        # Create messages list for the LLM
        messages = [
            SystemMessage(content=self.system_prompt),
            *chat_history
        ]
        
        # Run the LLM to get routing decision
        response = self.llm.with_structured_output(Router).invoke(messages)
        goto = response['next']
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    def evgeniy_node(self, state: State) -> Command[Literal["supervisor"]]:
        goto = 'supervisor'
        result = self.evgeniy_agent.invoke(state["messages"])

        if isinstance(state["messages"][-1], AIMessage):
            goto = 'evgeniy'

        return Command(
            update={"messages": result["messages"]},
            goto=goto,
        )

    def volodya_node(self, state: State) -> Command[Literal["supervisor"]]:
        goto = 'supervisor'
        result = self.volodya_agent.invoke(state["messages"])

        if isinstance(state["messages"][-1], AIMessage):
            goto = 'volodya'

        if "test_suite" in result:
            print("\nСгенерированные тест-кейсы:")
            print(result["test_suite"].json(indent=2, ensure_ascii=False))
        return Command(
            update={"messages": result["messages"]},
            goto=goto,
        )

    def upload_node(self, state: State) -> Command[Literal["supervisor"]]:
        goto = 'supervisor'
        result = self.upload_agent.invoke(state["messages"])

        if isinstance(state["messages"][-1], AIMessage):
            goto = 'upload'

        return Command(
            update={"messages": result["messages"]},
            goto=goto,
        )

    def invoke(self, state: State, config: dict) -> State:
        return self.graph.invoke(state, config=config)