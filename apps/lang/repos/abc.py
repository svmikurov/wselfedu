"""Abstract base classes for Language discipline repositories."""

from abc import ABC, abstractmethod
from typing import NamedTuple, TypedDict

from apps.users.models import CustomUser

from .. import types


class CreationStatus(NamedTuple):
    """Status of create English word translation."""

    created_native: bool
    created_english: bool
    created_translation: bool


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
        params: types.ParamOptionsT,
    ) -> types.WordStudyParams:
        """Get candidates for Presentation."""

    @abstractmethod
    def get_case(
        self,
        user: CustomUser,
        translation_id: int,
        language: types.LanguageType,
    ) -> types.PresentationDataT:
        """Get Presentation case."""


class WordStudyParamsRepositoryABC(ABC):
    """ABC for Word study params repository."""

    @abstractmethod
    def fetch(self, user: CustomUser) -> types.WordPresentationParamsT:
        """Fetch initial params."""

    @abstractmethod
    def update(
        self,
        user: CustomUser,
        data: types.UpdateParametersT,
    ) -> types.WordPresentationParamsT:
        """Update initial parameters."""


class TranslationRepoABC(ABC):
    """ABC for Get translation repository."""

    @abstractmethod
    def create_translation(
        self,
        user: CustomUser,
        native: str,
        english: str,
    ) -> CreationStatus:
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
