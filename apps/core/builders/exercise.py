"""Exercise case DTO null builder."""

from typing import Protocol, TypeVar

from apps.core.domains.exercise.dto import ExerciseDomainResultDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.presentation.dto import PresentationTask
from apps.core.domains.exercise.protocol import (
    ExerciseProcessResultProtocol,
    HasExerciseStatus,
)

DomainT = TypeVar('DomainT', bound=HasExerciseStatus)
DomainT_contra = TypeVar('DomainT_contra', contravariant=True)
SpecT = TypeVar('SpecT')
SpecT_contra = TypeVar('SpecT_contra', contravariant=True)
ResultT = TypeVar('ResultT', bound=HasExerciseStatus)
ResultT_co = TypeVar('ResultT_co', bound=HasExerciseStatus, covariant=True)


class CaseBuilderProtocol(
    Protocol[
        DomainT_contra,
        SpecT_contra,
        ResultT_co,
    ]
):
    """Protocol for exercise create result DTO interface."""

    def build(
        self,
        case: DomainT_contra,
        spec: SpecT_contra,
    ) -> ResultT_co:
        """Build exercise create result DTO."""


class ExerciseCaseNullBuilder(
    CaseBuilderProtocol[DomainT, SpecT, DomainT],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        case: DomainT,
        spec: SpecT,
    ) -> DomainT:
        """Build exercise case DTO."""
        return case


class ExercisePresentationBuilder(
    CaseBuilderProtocol[DomainT, SpecT, PresentationTask],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        case: DomainT,
        spec: SpecT,
    ) -> PresentationTask:
        """Build exercise case DTO."""
        return PresentationTask(
            status=case.status,
            question_text=case.case.option.define,  # type: ignore[attr-defined]
            answer_text=case.case.option.mean,  # type: ignore[attr-defined]
            progress_value=case.case.option.progress,  # type: ignore[attr-defined]
        )


class ExerciseCaseBuilder(
    CaseBuilderProtocol[
        DomainT, SpecT, ExerciseProcessResultProtocol[DomainT]
    ],
):
    """Exercise case DTO builder."""

    def build(
        self,
        case: DomainT,
        spec: SpecT,
    ) -> ExerciseProcessResultProtocol[DomainT]:
        """Build exercise case DTO."""
        return ExerciseDomainResultDTO(
            status=ExerciseStatusEnum.NEW_TASK,
            case=case,
        )
