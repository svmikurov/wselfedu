"""Exercise builders."""

from typing import TypeVar

from contracts.entity.domain.exercise.fields import HasExerciseStatus
from contracts.entity.general import NullProtocol

from ..null import NullSpecDtoBuilder

TaskT = TypeVar('TaskT', bound=HasExerciseStatus)


NullExerciseSpecDtoBuilder = NullSpecDtoBuilder[TaskT, NullProtocol]
"""Null exercise task DTO builder.
"""
