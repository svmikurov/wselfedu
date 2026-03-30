"""Typed request data."""

from typing import TypedDict

from apps.core.domains.exercise.enums import ExerciseProcessEnum


class ProcessExerciseWebData(TypedDict):
    """Process exercise WEB request typed data."""

    action: ExerciseProcessEnum
