"""Assigned exercise completion service."""

from typing import override

from django.db.models import Manager

from apps.math.models.calculation_condition import StudentCalculationCondition
from apps.math.services.abstract import AbstractCompletionService
from utils import decorators


class CalculationCompletionService(
    AbstractCompletionService[StudentCalculationCondition]
):
    """Assigned calculation exercise completion service."""

    def __init__(
        self,
        manager: Manager[StudentCalculationCondition],
    ) -> None:
        """Construct the service."""
        self._manager = manager

    @override
    @decorators.log_unimplemented_call
    def add_success(self, assignation_pk: int) -> None:
        """Add a successful attempt to solve the exercise."""

    @override
    @decorators.log_unimplemented_call
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""

    @property
    def manager(self) -> Manager[StudentCalculationCondition]:
        """Get assigned exercise manager."""
        return self._manager
