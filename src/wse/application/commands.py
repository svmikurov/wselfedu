"""Commands."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateTestingTask:
    """Command for create a testing task."""

    session_id: str


@dataclass(frozen=True, slots=True)
class CheckTestingAnswer:
    """Command for check a testing answer."""

    session_id: str
    answer_value: int
