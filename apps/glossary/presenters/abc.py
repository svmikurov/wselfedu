"""Abstract base classes for Glossary discipline app."""

from abc import ABC, abstractmethod
from typing import override

from apps.core.presenters.abc import StudyPresenterGenABC

from ..types import TermParamsType, TermType


class TermStudyPresenterABC(
    StudyPresenterGenABC[TermParamsType, TermType],
    ABC,
):
    """ABC fore Term study presenter."""

    @abstractmethod
    @override
    def get_presentation(self, params: TermParamsType) -> TermType:
        """Get Term study presentation case."""
