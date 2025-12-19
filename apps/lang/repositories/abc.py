"""Abstract base classes for Language discipline repositories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.core import models as core_models
    from apps.users.models import Person

    from .. import models, types


class ProgressABC(ABC):
    """ABC for Word study Progress repository."""

    @abstractmethod
    def update(
        self,
        user: Person,
        translation_id: int,
        language: types.Language,
        progress_delta: int,
    ) -> None:
        """Update Word study Progress."""


class PresentationABC(ABC):
    """ABC for Word study Presentation repo."""

    @abstractmethod
    def get_candidates(
        self,
        params: types.CaseParameters,
    ) -> types.WordStudyParameters:
        """Get candidates for Presentation."""

    @abstractmethod
    def get_word_study_data(
        self,
        user: Person,
        translation_id: int,
        language: types.Language,
    ) -> types.PresentationDataT:
        """Get Presentation case word data."""


class WordStudyParamsRepositoryABC(ABC):
    """ABC for Word study params repository."""

    @abstractmethod
    def fetch(self, user: Person) -> types.CaseSettings:
        """Fetch initial params."""

    @abstractmethod
    def get_options(self, user: Person) -> types.Options:
        """Get word study options."""

    @abstractmethod
    def update(
        self,
        user: Person,
        data: types.CaseParameters,
    ) -> types.CaseSettings:
        """Update initial parameters."""

    @abstractmethod
    def get_task_settings(self, user: Person) -> dict[str, Any]:
        """Get task settings."""


class TranslationRepoABC(ABC):
    """ABC for English translation repository."""

    @abstractmethod
    def create(
        self,
        user: Person,
        native: str,
        english: str,
        category: models.LangCategory,
        source: core_models.Source,
        marks: QuerySet[models.LangMark],
        normalize: bool = True,
    ) -> None:
        """Create English translation."""

    @abstractmethod
    def update(
        self,
        user: Person,
        instance: models.EnglishTranslation,
        native: str,
        english: str,
        category: models.LangCategory,
        source: core_models.Source,
        marks: QuerySet[models.LangMark],
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
