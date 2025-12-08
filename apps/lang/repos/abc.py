"""Abstract base classes for Language discipline repositories."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .. import types

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person

    from .. import models


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
        params: types.WordParameters,
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
    def fetch(self, user: Person) -> types.SetStudyParameters:
        """Fetch initial params."""

    @abstractmethod
    def update(
        self,
        user: Person,
        data: types.StudyParameters,
    ) -> types.SetStudyParameters:
        """Update initial parameters."""


class TranslationRepoABC(ABC):
    """ABC for Get translation repository."""

    @abstractmethod
    def create_translation(
        self,
        user: Person,
        native: str,
        english: str,
    ) -> None:
        """Create English word translation."""

    @abstractmethod
    def get_translation_id(
        self,
        word_id: int,
    ) -> int:
        """Get word translation.

        Parameters
        ----------
        word_id : `int`
            Word ID to translate.

        """

    @abstractmethod
    def get_translations(
        self,
        user: Person,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get English word translations."""
