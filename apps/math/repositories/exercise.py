"""Calculation exercise repository."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Manager
from django.shortcuts import get_object_or_404

from apps.core.handlers.protocol import DetailParamsProtocol
from apps.math.domains.dto import CalculationConditions

if TYPE_CHECKING:
    from apps.math.models import (
        AssignedCalculationCondition,
        CalculationCondition,
    )

__all__ = [
    'CalculationConditionsRepository',
    'StudentCalculationConditionsRepository',
]


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


class StudentCalculationConditionsRepository:
    """Student's assigned calculation conditions repository."""

    def __init__(self, manager: Manager[AssignedCalculationCondition]) -> None:
        """Construct the repository."""
        self._manager = manager

    def fetch(
        self, params: DetailParamsProtocol, user_pk: int
    ) -> CalculationConditions:
        """Fetch calculation exercise conditions."""
        # OPTIMIZE: Add prefetch related
        query = get_object_or_404(
            self._manager,
            pk=params.pk,
            mentorship__student__pk=user_pk,
        ).calculation_condition
        return CalculationConditions(
            min_operand=query.min_operand,
            max_operand=query.max_operand,
            operation_type=query.operation_type,  # type: ignore[arg-type]
        )
