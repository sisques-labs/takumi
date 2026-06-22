from dataclasses import dataclass

from takumi.contexts.team.prompt_template import PromptTemplate


@dataclass(frozen=True)
class AgentConfig:
    name: str
    role: str
    prompt_template: PromptTemplate

    @property
    def system_prompt(self) -> str:
        """Render the agent's system prompt from its configurable template."""
        return self.prompt_template.render(role=self.role, name=self.name)
