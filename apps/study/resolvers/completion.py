"""Exercise completion resolver."""

from typing import override

from django.utils import timezone

from apps.study.models import PeriodExecuting

from .abstract import AbstractCompletionResolver
from .protocol import CompletionStateDataType, SuccessCountDataType


class CompletionResolver(AbstractCompletionResolver):
    """Exercise completion resolver."""

    @override
    def get_completion_state(self, exercise: CompletionStateDataType) -> bool:
        """Resolve exercise perform success count."""
        match exercise.period_type:  # type: ignore[attr-defined]
            case PeriodExecuting.APPOINTMENT:
                return bool(exercise.is_completed)  # type: ignore[attr-defined]
            case PeriodExecuting.DAILY:
                return bool(
                    exercise.required_count == exercise.success_count  # type: ignore[attr-defined]
                    and exercise.tracking_date == timezone.now().date()  # type: ignore[attr-defined]
                )
            case _ as unexpected:
                raise ValueError(f'Unexpected period type {unexpected!r}')

    @override
    def get_success_count(self, exercise: SuccessCountDataType) -> int:
        """Resolve exercise perform success count."""
        match exercise.period_type:  # type: ignore[attr-defined]
            case PeriodExecuting.APPOINTMENT:
                # REVIEW: Check implementation
                return exercise.success_count or 0  # type: ignore[attr-defined]
            case PeriodExecuting.DAILY:
                if exercise.tracking_date == timezone.now().date():  # type: ignore[attr-defined]
                    return exercise.success_count or 0  # type: ignore[attr-defined]
                else:
                    return 0
            case _ as unexpected:
                raise ValueError(f'Unexpected period type {unexpected!r}')
