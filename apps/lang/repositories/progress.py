"""Abstract base class for Update word study repository."""

from typing import override

from apps.lang import types

from .abc import UpdateWordProgressRepoABC


class UpdateWordProgressRepo(UpdateWordProgressRepoABC):
    """Update word study repository."""

    @override
    def update(
        self,
        translation_id: int,
        language: types.LanguageType,
        progress_case: types.ProgressType,
        progress_value: int,
    ) -> None:
        """Update word study progress."""
