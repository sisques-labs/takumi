import pytest

from takumi.contexts.orchestration.workflow import WORKFLOW_ORDER
from takumi.contexts.team.prompt_loader import available_prompts, load_prompt_template
from takumi.contexts.team.prompt_template import PromptTemplate
from takumi.contexts.team.roles import AGENT_ROLES

EXPECTED_AGENTS = {"architect", "backend", "frontend", "qa"}


def test_roster_matches_expected_agents() -> None:
    assert set(AGENT_ROLES) == EXPECTED_AGENTS


def test_workflow_order_covers_roster() -> None:
    assert set(WORKFLOW_ORDER) == EXPECTED_AGENTS


def test_po_agent_is_out_of_scope() -> None:
    # PO agent prompt is covered by TAKUMI-15, not this story.
    assert "po" not in AGENT_ROLES


def test_every_agent_has_a_detailed_prompt() -> None:
    for agent in AGENT_ROLES.values():
        prompt = agent.system_prompt
        assert prompt.strip(), f"{agent.name} has an empty prompt"
        assert len(prompt) > 200, f"{agent.name} prompt is not detailed enough"


def test_prompts_are_distinct() -> None:
    prompts = [agent.system_prompt for agent in AGENT_ROLES.values()]
    assert len(set(prompts)) == len(prompts)


def test_role_placeholder_is_substituted() -> None:
    for agent in AGENT_ROLES.values():
        assert agent.role in agent.system_prompt
        assert "$role" not in agent.system_prompt


@pytest.mark.parametrize(
    ("agent_name", "keywords"),
    [
        ("architect", ["design", "tech stack", "trade-off"]),
        ("backend", ["API", "data model", "server-side"]),
        ("frontend", ["component", "UX", "accessib"]),
        ("qa", ["test strategy", "edge case", "coverage"]),
    ],
)
def test_prompt_reflects_role_focus(agent_name: str, keywords: list[str]) -> None:
    prompt = AGENT_ROLES[agent_name].system_prompt.lower()
    for keyword in keywords:
        assert keyword.lower() in prompt, f"{agent_name} prompt missing '{keyword}'"


def test_available_prompts_lists_all_templates() -> None:
    assert EXPECTED_AGENTS <= set(available_prompts())


def test_load_prompt_template_unknown_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_prompt_template("does-not-exist")


def test_prompt_template_renders_placeholders() -> None:
    template = PromptTemplate(name="demo", template="Hello $role, task $missing")
    rendered = template.render(role="Architect")
    assert "Hello Architect" in rendered
    # Unknown placeholders are left intact rather than raising.
    assert "$missing" in rendered
