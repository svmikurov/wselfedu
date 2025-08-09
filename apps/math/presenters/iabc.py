"""Defines protocols and ABC for Math app presenter interfaces."""

from abc import ABC, abstractmethod
from typing import Protocol, Any

from typing_extensions import override


class ICalcPresenter(Protocol):
    """Protocol for calculation task presenter interface."""

    def get_task(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get calculation task."""

    def get_result(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get user answer checking result."""


class CalcPresenterABC(ICalcPresenter, ABC):
    """Abstract base class for calculation task presenter."""

    @abstractmethod
    @override
    def get_task(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get calculation task."""

    @abstractmethod
    @override
    def get_result(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get user answer checking result."""