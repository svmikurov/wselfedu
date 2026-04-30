"""Language discipline DTO factory."""

from typing import override

from apps.core.builders.abstract import AbstractCaseFactory
from contracts.schemas.domain.exercise.dtos import (
    PresentationTask,
)


# HACK: Simple implementation
class PresentationDTOFactory(
    AbstractCaseFactory[PresentationTask, PresentationTask]
):
    """Presentation case DTO factory."""

    @override
    def build(
        self,
        option: PresentationTask,
    ) -> PresentationTask:
        """Build presentation exercise DTO."""
        return option
