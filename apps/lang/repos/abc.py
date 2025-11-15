"""Abstract base classes for Language discipline repositories."""

from abc import ABC, abstractmethod
from typing import TypedDict

from apps.users.models import CustomUser

from .. import types


class ProgressABC(ABC):
    """ABC for Word study Progress repository."""

    class UpdateResult(TypedDict):
        """Word study Progress update result typed dict."""

        created: bool
        current_progress: int

    @abstractmethod
    def update(
        self,
        user: CustomUser,
        translation_id: int,
        language: types.LanguageType,
        progress_delta: int,
    ) -> UpdateResult:
        """Update Word study Progress."""


class PresentationABC(ABC):
    """ABC for Word study Presentation repo."""

    @abstractmethod
    def get_candidates(
        self,
        params: types.WordParamsType,
    ) -> types.WordStudyParams:
        """Get candidates for Presentation."""

    @abstractmethod
    def get_word_data(
        self,
        english_word_id: int,
        user: CustomUser,
    ) -> types.WordDataType:
        """Get Presentation case."""


class WordStudyParamsRepositoryABC(ABC):
    """ABC for Word study params repository."""

    @abstractmethod
    def fetch_initial(self, user: CustomUser) -> types.WordParamsType:
        """Fetch initial params."""


class TranslationRepoABC(ABC):
    """ABC for Get translation repository."""

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
