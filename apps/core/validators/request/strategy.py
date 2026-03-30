"""Exercise process validator strategy."""

from typing import Any

from apps.core.domains.exercise.dto import ExerciseStatusSchema
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.handlers.protocol import RequestDataProtocol

from .abstract import AbstractRequestValidator
from .protocol import TestExerciseAnswerProtocol


class ExerciseValidatorStrategy(
    AbstractRequestValidator[
        RequestDataProtocol[dict[str, Any]],
        TestExerciseAnswerProtocol,
    ]
):
    """Exercise process validator strategy."""

    def __init__(
        self,
        registry: dict[
            ExerciseStatusEnum,
            AbstractRequestValidator[Any, Any],
        ],
    ) -> None:
        """Construct the strategy."""
        self._registry = registry

    def validate(
        self,
        data: RequestDataProtocol[dict[str, Any]],
    ) -> TestExerciseAnswerProtocol:
        """Validate test exercise user's answer data."""
        process = ExerciseStatusSchema(status=data.data['exercise_status'])
        strategy = self._registry[process.status]
        return strategy.validate(data)  # type: ignore
