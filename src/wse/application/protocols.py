"""Application layer protocols."""

from typing import Protocol, TypeVar

from wse.domain import enums

T_cov = TypeVar('T_cov', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


class HasTask(Protocol[T_cov]):
    @property
    def task(self) -> T_cov: ...


class HasExerciseAction(Protocol):
    @property
    def exercise_action(self) -> enums.ExerciseAction: ...


class HasSessionIdentifier(Protocol):
    @property
    def session_id(self) -> str: ...


class HasIsCorrect(Protocol):
    @property
    def is_correct(self) -> bool: ...


class HasAnswerValue(Protocol):
    @property
    def answer_value(self) -> int: ...


###################################################
# Commands
###################################################


class TaskCommandProto(
    HasExerciseAction,
    HasSessionIdentifier,
    Protocol,
): ...


class CheckTestingCommandProto(
    TaskCommandProto,
    HasAnswerValue,
    Protocol,
): ...


###################################################
# DTOs
###################################################


class TaskDtoProto(
    HasTask[T_cov],
    HasSessionIdentifier,
    Protocol[T_cov],
): ...


class CheckResultDtoProto(
    HasIsCorrect,
    Protocol,
): ...


###################################################
# Use cases
###################################################


class Executable(Protocol[T_contra, T_cov]):
    def execute(self, cmd: T_contra) -> T_cov: ...
