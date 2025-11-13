"""Abstract base classes for Language discipline."""

from abc import ABC, abstractmethod

from apps.users.models import CustomUser

from .. import types


class UpdateWordProgressRepoABC(ABC):
    """ABC for Update word study repository."""

    @abstractmethod
    def update(
        self,
        user: CustomUser,
        translation_id: int,
        language: types.LanguageType,
        progress_delta: int,
    ) -> dict[str, int | bool]:
        """Update word study progress."""


class WordStudyRepositoryABC(ABC):
    """ABC for word study repository."""

    @abstractmethod
    def get_candidates(
        self,
        params: types.WordParamsType,
    ) -> types.WordStudyParams:
        """Get candidates of words to study."""

    @abstractmethod
    def get_word_data(
        self,
        english_word_id: int,
        user: CustomUser,
    ) -> types.WordDataType:
        """Get items for exercise case."""


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
