"""Domain result schemas."""

from typing import Generic, TypeVar

from interfaces.enums.exercise import ExerciseStatus
from interfaces.schemas.base import ArbitraryDTO

DomainResult = TypeVar('DomainResult')


class ExerciseDomainResultDTO(ArbitraryDTO, Generic[DomainResult]):
    """Exercise domain result DTO."""

    status: ExerciseStatus
    case: DomainResult
