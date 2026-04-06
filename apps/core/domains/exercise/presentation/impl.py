"""Domain logic for selecting items for presentation cases."""

from random import choice
from typing import TypeVar

from apps.core.factories.protocol import CaseFactoryProtocol

from ..abstract import AbstractConfigurableCandidatesExerciseDomain
from ..enums import DisplayOrder, ExerciseStatusEnum
from ..protocol import (
    Candidate,
    Candidates,
    HasDisplayOrder,
    SelectorProtocol,
)
from .dto import PresentationCase, PresentationMeta

__all__ = ('PresentationDomain',)

ConfT = HasDisplayOrder
CaseT = Candidate
TaskT = TypeVar('TaskT')


# IDEA: Experimental impl
class TaskPresentationDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        ConfT,
        TaskT,
    ],
):
    """Presentation exercise domain logic."""

    def __init__(
        self,
        selector: SelectorProtocol[HasDisplayOrder],
        factory: CaseFactoryProtocol[ConfT, CaseT, TaskT],
    ) -> None:
        """Configure the domain."""
        self._selector = selector
        self._factory = factory

    def execute(
        self,
        candidates: Candidates,
        conf: ConfT,
    ) -> TaskT:
        """Get presentation exercise case data."""
        selected_candidates = self._selector.select(candidates, conf)

        case = choice(selected_candidates)
        task = self._factory.build(conf, case)

        return task


# DEPRECATED: Combine meta and case
class PresentationDomain(
    AbstractConfigurableCandidatesExerciseDomain[
        HasDisplayOrder,
        tuple[PresentationCase, PresentationMeta],
    ],
):
    """Presentation exercise domain logic."""

    def __init__(
        self,
        selector: SelectorProtocol[HasDisplayOrder],
        # factory: DTOFactoryProtocol,
    ) -> None:
        """Configure the domain."""
        self._selector = selector
        # self._factory = factory

    def execute(
        self,
        candidates: Candidates,
        conf: HasDisplayOrder,
    ) -> tuple[PresentationCase, PresentationMeta]:
        """Get presentation exercise case data."""
        selected_candidates = self._selector.select(candidates, conf)

        task = choice(selected_candidates)

        case = self._build_case(task, conf.display_order)
        meta = self._build_meta(task)
        return case, meta

    @staticmethod
    def _build_case(
        task: Candidate,
        order: DisplayOrder,
    ) -> PresentationCase:
        """Build exercise case DTO to rendering."""
        question, answer = order.get_display_phases()
        return PresentationCase(
            status=ExerciseStatusEnum.NEW_CASE,
            question_text=getattr(task, question),
            answer_text=getattr(task, answer),
            progress_value=task.progress,
        )

    @staticmethod
    def _build_meta(candidate: Candidate) -> PresentationMeta:
        """Build exercise case metadata DTO for internal tracking."""
        return PresentationMeta(pk=candidate.pk)
