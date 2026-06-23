from pydantic import BaseModel, Field


class AcceptanceCriteria(BaseModel):
    number: int
    description: str


class UserStory(BaseModel):
    as_a: str = Field(description="The user or persona who needs this")
    i_want: str = Field(description="The capability or feature desired")
    so_that: str = Field(description="The benefit or goal achieved")
    acceptance_criteria: list[AcceptanceCriteria] = Field(
        description="Numbered acceptance criteria for this story"
    )


class Epic(BaseModel):
    title: str = Field(description="Short title for the epic")
    goal: str = Field(description="Clear goal statement describing the epic's purpose")
    stories: list[UserStory] = Field(
        description="2 to 5 user stories belonging to this epic",
        min_length=2,
        max_length=5,
    )


class BacklogArtifact(BaseModel):
    feature_description: str = Field(description="The original raw feature description")
    epics: list[Epic] = Field(description="One or more epics generated from the feature")
