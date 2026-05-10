"""Language discipline DTO factory."""

from typing import override

from contracts.schemas.domain.exercise.flow import (
    PresentationTask,
)
from ports.abstract.builder import AbstractCaseFactory


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
