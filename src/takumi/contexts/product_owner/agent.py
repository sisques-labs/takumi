from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from takumi.contexts.product_owner.models import BacklogArtifact

_SYSTEM_PROMPT = (
    "You are an experienced Product Owner. Given a raw feature description, "
    "you decompose it into structured epics and user stories ready for a development backlog. "
    "Each epic must have a clear goal statement. "
    "Each user story must follow the format: As a <user>, I want <capability>, so that <benefit>. "
    "Each story must include numbered acceptance criteria."
)


def run_po_agent(llm: BaseChatModel, feature_description: str) -> BacklogArtifact:
    structured_llm = llm.with_structured_output(BacklogArtifact)
    return structured_llm.invoke(
        [
            SystemMessage(content=_SYSTEM_PROMPT),
            HumanMessage(
                content=(
                    f"Feature description:\n\n{feature_description}\n\n"
                    "Generate epics and user stories for this feature."
                )
            ),
        ]
    )
