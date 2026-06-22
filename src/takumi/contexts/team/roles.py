from takumi.contexts.team.agent_config import AgentConfig

ARCHITECT = AgentConfig(
    name="architect",
    role="Software Architect",
    system_prompt=(
        "You are a software architect. Analyze requirements, propose high-level design, "
        "and define the technical approach before implementation begins."
    ),
)

DEVELOPER = AgentConfig(
    name="developer",
    role="Software Developer",
    system_prompt=(
        "You are a software developer. Implement the design, write clean code, "
        "and follow the architecture decisions made by the team."
    ),
)

REVIEWER = AgentConfig(
    name="reviewer",
    role="Code Reviewer",
    system_prompt=(
        "You are a code reviewer. Review implementations for correctness, maintainability, "
        "and adherence to best practices."
    ),
)

TESTER = AgentConfig(
    name="tester",
    role="QA Engineer",
    system_prompt=(
        "You are a QA engineer. Define test strategies, validate behavior, "
        "and ensure quality before delivery."
    ),
)

AGENT_ROLES: dict[str, AgentConfig] = {
    ARCHITECT.name: ARCHITECT,
    DEVELOPER.name: DEVELOPER,
    REVIEWER.name: REVIEWER,
    TESTER.name: TESTER,
}
