"""Calculation exercise repository."""

from django.db.models import Manager
from django.shortcuts import get_object_or_404

from apps.core.handlers.protocol import DetailParamsProtocol
from apps.math.domains.dto import CalculationConditions
from apps.math.models import CalculationCondition


class CalculationConditionsRepository:
    """Calculation conditions repository."""

    def __init__(self, manager: Manager[CalculationCondition]) -> None:
        """Construct the repository."""
        self._manager = manager

    def fetch(
        self, params: DetailParamsProtocol, user_pk: int
    ) -> CalculationConditions:
        """Fetch calculation exercise conditions."""
        query = get_object_or_404(self._manager, pk=params.pk, user_id=user_pk)
        return CalculationConditions(
            min_operand=query.min_operand,
            max_operand=query.max_operand,
            operation_type=query.operation_type,  # type: ignore[arg-type]
        )
