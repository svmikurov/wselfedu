"""Abstract base classes for Glossary discipline app."""

from abc import ABC, abstractmethod

from apps.users.models import Person

from ..types import TermParamsType, TermType


class TermStudyPresenterABC(
    ABC,
):
    """ABC fore Term study presenter."""

    @abstractmethod
    def get_case(
        self,
        user: Person,
        params: TermParamsType,
    ) -> TermType:
        """Get Term study presentation case."""
