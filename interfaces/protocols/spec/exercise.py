"""Protocols for exercise service specification interface."""

from typing import Protocol

from apps.core.domains.exercise.protocol import (
    HasExistingCase,
)
from contracts.entity.domain.exercise.fields import HasAnswer
from contracts.entity.domain.params import (
    HasConditions,
    HasConfig,
    HasSettings,
)
from interfaces.protocols.domain.exercise import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseSettingsProtocol,
    TestAnswerProtocol,
    TestDomainResultProtocol,
)


class CreateTaskSpecProtocol(
    HasConditions[ConditionsProtocol],
    HasConfig[ExerciseConfigProtocol],
    HasSettings[ExerciseSettingsProtocol],
    HasExistingCase[TestDomainResultProtocol],
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
    HasExistingCase[TestDomainResultProtocol],
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
