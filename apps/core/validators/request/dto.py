"""Validated data schemas."""

from apps.core.domains.dto import BaseDTO


class TestExerciseAnswerDTO(BaseDTO):
    """Test exercise answer DTO."""

    option_value: int
