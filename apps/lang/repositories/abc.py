"""Abstract base classes for Language discipline repositories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.core import models as core_models
    from apps.users.models import Person

    from .. import models, types


class RuleRepositoryABC(ABC):
    """ABC for rule repository."""

    @classmethod
    @abstractmethod
    def get_for_user(
        cls,
        user: Person,
        rule_id: int,
    ) -> models.Rule:
        """Get rule with all examples and exceptions."""


class ProgressABC(ABC):
    """ABC for Word study Progress repository."""

    @abstractmethod
    def update(
        self,
        user: Person,
        translation_id: int,
        progress_delta: int,
    ) -> None:
        """Update Word study Progress."""


class PresentationABC(ABC):
    """ABC for Word study Presentation repo."""

    @abstractmethod
    def get_candidates(
        self,
        parameters: types.CaseParametersAPI,
    ) -> types.CaseCandidates:
        """Get candidates for Presentation."""

    @abstractmethod
    def get_translation(
        self,
        user: Person,
        translation_id: int,
    ) -> types.PresentationDataT:
        """Get Presentation case word data."""


class StudyParametersRepositoryABC(ABC):
    """ABC for Word study params repository."""

    @abstractmethod
    def fetch(self, user: Person) -> types.CaseSettingsAPI:
        """Fetch initial params."""

    @abstractmethod
    def get_options(self, user: Person) -> types.OptionsAPI:
        """Get word study options."""

    @abstractmethod
    def update(
        self,
        user: Person,
        data: types.CaseParametersAPI,
    ) -> types.CaseSettingsAPI:
        """Update initial parameters."""


class TranslationRepoABC(ABC):
    """ABC for English translation repository."""

    @abstractmethod
    def create(
        self,
        user: Person,
        native: str,
        foreign: str,
        category: models.Category,
        source: core_models.Source,
        marks: QuerySet[models.Mark],
        normalize: bool = True,
    ) -> None:
        """Create English translation."""

    @abstractmethod
    def update(
        self,
        user: Person,
        instance: models.EnglishTranslation,
        native: str,
        foreign: str,
        category: models.Category,
        source: core_models.Source,
        marks: QuerySet[models.Mark],
        normalize: bool = True,
    ) -> None:
        """Update English translation."""

    @abstractmethod
    def get_translation_id(
        self,
        native_id: int,
    ) -> int:
        """Get English translation ID by native word ID."""

    @abstractmethod
    def get_translations(
        self,
        user: Person,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get English translations."""
