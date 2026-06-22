from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from takumi.contexts.orchestration.state import TeamState
from takumi.contexts.team.roles import AGENT_ROLES

WORKFLOW_ORDER: list[str] = [
    "architect",
    "backend",
    "frontend",
    "qa",
]


def _make_agent_node(agent_name: str, llm: BaseChatModel):
    agent = AGENT_ROLES[agent_name]

    def node(state: TeamState) -> dict:
        response = llm.invoke(
            [
                SystemMessage(content=agent.system_prompt),
                HumanMessage(
                    content=(
                        f"Task: {state['task']}\n\n"
                        f"You are acting as the {agent.role}. "
                        "Provide your contribution to this task."
                    )
                ),
            ]
        )
        content = response.content if isinstance(response.content, str) else str(response.content)
        return {
            "current_agent": agent_name,
            "messages": [AIMessage(content=content, name=agent_name)],
            "artifacts": {agent_name: content},
        }

    return node


def build_workflow(llm: BaseChatModel):
    graph = StateGraph(TeamState)

    for agent_name in WORKFLOW_ORDER:
        graph.add_node(agent_name, _make_agent_node(agent_name, llm))

    graph.add_edge(START, WORKFLOW_ORDER[0])
    for current, next_agent in zip(WORKFLOW_ORDER, WORKFLOW_ORDER[1:], strict=False):
        graph.add_edge(current, next_agent)
    graph.add_edge(WORKFLOW_ORDER[-1], END)

    return graph.compile()


def run_workflow(llm: BaseChatModel, task: str) -> TeamState:
    workflow = build_workflow(llm)
    return workflow.invoke(
        {
            "task": task,
            "messages": [],
            "current_agent": "",
            "artifacts": {},
        }
    )
