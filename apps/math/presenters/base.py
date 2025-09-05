"""Protocols for Math app presenters."""

from abc import ABC

from apps.core.presenters import TaskPresenter
from apps.core.types import ResultType

from ..services.types import (
    CalcAnswerType,
    CalcConditionType,
    CalcTaskType,
)


class BaseCalcTaskPresenter(
    TaskPresenter[
        CalcConditionType,
        CalcTaskType,
        CalcAnswerType,
        ResultType,
    ],
    ABC,
):
    """Typed base class for calculation task presenter."""
