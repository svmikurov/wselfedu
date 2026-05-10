"""Protocols for exercise service specification interface."""

from typing import Protocol

from interfaces.protocols.domain.exercise import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseSettingsProtocol,
    TestAnswerProtocol,
    TestDomainResultProtocol,
)
from ports.contract.entity.domain.exercise.fields import HasAnswer, HasCase
from ports.contract.entity.domain.params import (
    HasConditions,
    HasConfig,
    HasSettings,
)


class CreateTaskSpecProtocol(
    HasConditions[ConditionsProtocol],
    HasConfig[ExerciseConfigProtocol],
    HasSettings[ExerciseSettingsProtocol],
    HasCase[TestDomainResultProtocol],
    Protocol,
):
    """Protocol for create task service specification interface.

    Parameters
    ----------
    conditions : `ConditionsProtocol`
        Item study database lockup conditions.
    conf : `ExerciseConfigProtocol`
        Exercise creating configuration.
    settings : `ExerciseSettingsProtocol`
        Task display settings.
    existing_case : `TestDomainResultProtocol` | None
        Stored performing task.
        Exercise logic validates new task request only
        after the current task has been completed.

    """


class CheckTestSpecProtocol(
    HasAnswer[TestAnswerProtocol],
    HasCase[TestDomainResultProtocol],
    Protocol,
):
    """Protocol for check test task service specification interface.

    Parameters
    ----------
    answer : `TestAnswerProtocol`
        User answer.
    case : `TestDomainResultProtocol` | None
        Stored performing test task, domain result.

    """
