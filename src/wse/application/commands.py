"""Commands."""

from dataclasses import dataclass

from wse.domain.enums import ExerciseAction


@dataclass(frozen=True, slots=True)
class TaskPerform:
    """Command for create a testing task."""

    session_id: str
    exercise_action: ExerciseAction = ExerciseAction.CREATE_TASK


@dataclass(frozen=True, slots=True)
class CheckTestingAnswer:
    """Command for check a testing answer."""

    session_id: str
    answer_value: int
    exercise_action: ExerciseAction = ExerciseAction.CHECK_ANSWER
