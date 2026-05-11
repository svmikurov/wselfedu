"""Language discipline DTO factory."""

from typing import override

from ports.abstract.builder import AbstractCaseFactory
from ports.interfaces.schemas.domain.exercise.flow import (
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
