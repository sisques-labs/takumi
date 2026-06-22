from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class TeamState(TypedDict):
    task: str
    messages: Annotated[list[BaseMessage], add_messages]
    current_agent: str
    artifacts: dict[str, str]
