"""Calculation exercise use case."""

from apps.core.handlers.abstract import AbstractSimpleHandler
from apps.users.models.user import Person

from .dto import CalculationConditionsDTO


class CalculationConditionsUseCase(
    AbstractSimpleHandler[CalculationConditionsDTO],
):
    """Calculation conditions use case."""

    def execute(self, user: Person) -> CalculationConditionsDTO:
        """Return calculation exercise conditions."""
        return CalculationConditionsDTO()
