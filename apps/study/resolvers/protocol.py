"""Study app resolver protocol."""

from datetime import datetime
from typing import Protocol, TypedDict

from apps.study.models import PeriodExecuting


class CompletionStateDataType(TypedDict):
    """Completion state data type."""

    period_type: PeriodExecuting
    is_completed: bool
    required_count: int
    success_count: int
    tracking_date: datetime


class SuccessCountDataType(TypedDict):
    """Success count completion data type."""

    period_type: PeriodExecuting
    success_count: int
    tracking_date: datetime


class CompletionResolverProtocol(Protocol):
    """Protocol for exercise completion resolver interface."""

    def get_completion_state(self, exercise: CompletionStateDataType) -> bool:
        """Resolve exercise completion state."""

    def get_success_count(self, exercise: SuccessCountDataType) -> int:
        """Resolve exercise perform success count."""
