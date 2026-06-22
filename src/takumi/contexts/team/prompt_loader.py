from functools import cache
from importlib import resources

from takumi.contexts.team.prompt_template import PromptTemplate

PROMPTS_PACKAGE = "takumi.contexts.team.prompts"


@cache
def load_prompt_template(name: str) -> PromptTemplate:
    """Load a prompt template by name from the ``prompts`` package.

    Templates are stored as ``prompts/<name>.md`` files, keeping prompt content
    configurable and editable outside of Python source.

    Raises:
        FileNotFoundError: if no template file exists for ``name``.
    """
    resource = resources.files(PROMPTS_PACKAGE) / f"{name}.md"
    if not resource.is_file():
        raise FileNotFoundError(f"No prompt template found for '{name}' ({resource})")
    return PromptTemplate(name=name, template=resource.read_text(encoding="utf-8"))


def available_prompts() -> list[str]:
    """Return the names of all bundled prompt templates."""
    return sorted(
        entry.name.removesuffix(".md")
        for entry in resources.files(PROMPTS_PACKAGE).iterdir()
        if entry.name.endswith(".md")
    )
