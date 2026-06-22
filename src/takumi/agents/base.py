from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    name: str
    role: str
    system_prompt: str
