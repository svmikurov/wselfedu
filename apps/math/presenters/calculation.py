"""Defines simple calculation exercise presenter."""

from ..services.types import CalcAnswerType
from .base import BaseCalcTaskPresenter


class CalculationPresenter(
    BaseCalcTaskPresenter[CalcAnswerType],
):
    """Calculation task presenter."""
