"""Protocols for application layer interface."""

from typing import Protocol, TypeVar

from wse.domain.protocols import ExerciseCommandProto, ExerciseResultProto

TaskT = TypeVar('TaskT', covariant=True)


class ExecutableExercise(Protocol[TaskT]):
    def execute(
        self,
        command: ExerciseCommandProto,
    ) -> ExerciseResultProto[TaskT]: ...
