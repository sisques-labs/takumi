from dataclasses import dataclass
from string import Template


@dataclass(frozen=True)
class PromptTemplate:
    """A configurable system prompt loaded from an external template.

    The template body may contain ``$variable`` placeholders (see
    :class:`string.Template`) that are substituted at render time. This keeps
    prompt content decoupled from code so prompts can be edited, versioned, or
    overridden without touching Python source.
    """

    name: str
    template: str

    def render(self, **variables: str) -> str:
        """Render the template, substituting any ``$variable`` placeholders.

        Unknown placeholders are left untouched so a partially parameterized
        template never raises at render time.
        """
        return Template(self.template).safe_substitute(**variables).strip()
