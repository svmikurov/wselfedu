"""Abstract base class for Update word study repository."""

from typing import override

from apps.lang import types
from utils import decorators

from .abc import UpdateWordProgressRepoABC


class UpdateWordProgressRepo(UpdateWordProgressRepoABC):
    """Update word study repository."""

    @override
    @decorators.log_unimplemented_call
    def update(
        self,
        translation_id: int,
        language: types.LanguageType,
        progress_case: types.ProgressType,
        progress_value: int,
    ) -> None:
        """Update word study progress."""
