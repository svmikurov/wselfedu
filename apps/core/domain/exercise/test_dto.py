"""Test exercise domain DTOs (internal data transfer)."""

from __future__ import annotations

from pydantic import Field

from apps.core.domain.base_dto import BaseDTO, ProtectDefaultStatusMixin

from . import ExerciseStatusEnum, UuidDTO

# ---------------------
# Test exercise options
# ---------------------


class Option(BaseDTO):
    """Test exercise case option."""

    value: int = Field(description='Option value for business logic')
    text: str = Field(description='Display option text')


class OptionMeta(BaseDTO):
    """Test exercise case option mapping with item ID."""

    pk: int = Field(description='Database item ID')
    value: int = Field(description='Option value for business logic')
    define: str = Field(description='Question item text')
    explain: str = Field(description='Answer item text')


# ----------------------------------
# Create test exercise domain result
# ----------------------------------


class TestExerciseCase(ProtectDefaultStatusMixin, BaseDTO):
    """Test exercise case."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE,
        description='Exercise status',
    )

    question_text: str = Field(
        description='Display question text',
    )
    answer_text_options: list[Option] = Field(
        description='Display answer text options'
    )


class TestExerciseMeta(ProtectDefaultStatusMixin, BaseDTO):
    """Test exercise meta to store for answer handle."""

    pk: int = Field(description='Database question item ID')
    question_text: str = Field(
        description='Display question text',
    )
    answer_text: str = Field(
        description='Display answer text',
    )
    option_value: int = Field(
        description='Correct answer option value',
    )
    options: list[OptionMeta] = Field(
        description='Extended option data',
    )

    def get_question_text(self, value: int) -> str:
        """Get option question text by value."""
        return self.options[value].define

    def get_answer_text(self, value: int) -> str:
        """Get option answer text by value."""
        return self.options[value].explain


class TestExerciseData(UuidDTO, TestExerciseCase):
    """Test exercise case for rendering to the user."""


# ---------------------------------
# Check test exercise domain result
# ---------------------------------


class TestExerciseResult(BaseDTO):
    """User's answer check on test exercise question."""

    is_correct: bool = Field(
        description="Is correct the user's answer",
    )

    # Current question & correct answer
    question_text: str = Field(
        description='Original question text',
    )
    answer_text: str = Field(
        description='Correct answer text on original question',
    )
    # User answer selection & question for user selection
    selected_question_text: str = Field(
        description='Question text for user answer text option select',
    )
    selected_answer_text: str = Field(
        description='User answer text option select',
    )


class TestExerciseExplanation(ProtectDefaultStatusMixin, BaseDTO):
    """Test exercise case correct answer explanation."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.EXPLAIN,
        description='Exercise status',
    )

    # Current question & correct answer
    question_text: str = Field(
        description='Original question text',
    )
    answer_text: str = Field(
        description='Correct answer text on original question',
    )
    # User answer selection & question for user selection
    selected_question_text: str = Field(
        description='Question text for user answer text option select',
    )
    selected_answer_text: str = Field(
        description='User answer text option select',
    )
