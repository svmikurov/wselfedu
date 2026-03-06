"""Protocols and ABC for Study app services."""

from abc import ABC, abstractmethod
from typing import Protocol

from typing_extensions import override


class StrTaskCheckerProto(Protocol):
    """Protocol for task checker service."""

    def check(self, correct_answer: str, user_answer: str) -> bool:
        """Check user answer."""


class BaseStrTaskChecker(ABC, StrTaskCheckerProto):
    """Abstract base class for string answer task checker."""

    @abstractmethod
    @override
    def check(self, correct_answer: str, user_answer: str) -> bool:
        """Check user answer."""
