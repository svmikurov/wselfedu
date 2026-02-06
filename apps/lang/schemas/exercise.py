"""Exercise schemas."""

from pydantic import BaseModel, Field

from apps.core.domain.exercise.test_dto import OptionMeta


class TestSettingsDTO(BaseModel):
    """Test exercise settings DTO."""

    display_order: str


class TestExerciseDTO(BaseModel):
    """Test exercise data DTO."""

    question_text: str = Field(description='Question object text to display')
    object_pk: int = Field(description='Question object DB identifier')

    answer_text: str = Field(description='Correct answer text')
    answer_value: int = Field(description='Correct answer option value')

    option_pks: list[OptionMeta] = Field(
        description='Match object pk vs option value'
    )
    option_texts: list[OptionMeta] = Field(
        description='Match object text vs option value'
    )
