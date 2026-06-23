from takumi.contexts.team.agent_config import AgentConfig
from takumi.contexts.team.prompt_loader import load_prompt_template

ARCHITECT = AgentConfig(
    name="architect",
    role="Software Architect",
    prompt_template=load_prompt_template("architect"),
)

BACKEND = AgentConfig(
    name="backend",
    role="Backend Engineer",
    prompt_template=load_prompt_template("backend"),
)

FRONTEND = AgentConfig(
    name="frontend",
    role="Frontend Engineer",
    prompt_template=load_prompt_template("frontend"),
)

QA = AgentConfig(
    name="qa",
    role="QA Engineer",
    prompt_template=load_prompt_template("qa"),
)

AGENT_ROLES: dict[str, AgentConfig] = {
    ARCHITECT.name: ARCHITECT,
    BACKEND.name: BACKEND,
    FRONTEND.name: FRONTEND,
    QA.name: QA,
}
