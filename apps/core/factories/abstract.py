"""Abstract base class for factories."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CaseDTO = TypeVar('CaseDTO')
ParametersDTO = TypeVar('ParametersDTO')
ResultDTO = TypeVar('ResultDTO')


class AbstractExerciseDTOFactory(
    ABC,
    Generic[CaseDTO, ParametersDTO, ResultDTO],
):
    """ABC for exercise DTO factory."""

    @abstractmethod
    def create(self, case: CaseDTO, parameters: ParametersDTO) -> ResultDTO:
        """Create exercise DTO."""
