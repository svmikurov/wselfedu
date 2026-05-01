"""Protocol for exercise process parameters adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from utils.audit.impl import NullAuditor
from utils.audit.protocol import AuditorProtocol

from .protocol import ExerciseProcessAdapterProtocol

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
ExistingCaseT = TypeVar('ExistingCaseT')
AdaptedT = TypeVar('AdaptedT')


class AbstractExerciseProcessAdapter(
    ABC,
    ExerciseProcessAdapterProtocol[
        CommandT,
        ParamsT,
        ExistingCaseT,
        AdaptedT,
    ],
):
    """Protocol for adapt parameters for exercise process interface."""

    def __init__(
        self,
        name: str | None = None,
        auditor: AuditorProtocol | None = None,
    ) -> None:
        """Construct the adapter."""
        self._name = name or 'undefined'
        self._auditor = auditor or NullAuditor()

    @override
    @abstractmethod
    def adapt(
        self,
        command: CommandT,
        params: ParamsT,
        existing_case: ExistingCaseT | None,
    ) -> AdaptedT:
        """Adapt for exercise precess execute."""

    @property
    def name(self) -> str:
        """Return adapter name."""
        return self._name
