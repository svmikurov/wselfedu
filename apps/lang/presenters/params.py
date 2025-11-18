"""Word study params presenter."""

from typing import override

from apps.users.models import CustomUser

from ..repos.abc import WordStudyParamsRepositoryABC
from ..types import WordParamsType
from .abc import (
    WordStudyParamsPresenterABC,
)


# TODO: Rename to repository
class WordStudyParamsPresenter(WordStudyParamsPresenterABC):
    """Word study params repository."""

    def __init__(
        self,
        repo: WordStudyParamsRepositoryABC,
    ) -> None:
        """Construct the presenter."""
        self._repo = repo

    @override
    def get_initial(self, user: CustomUser) -> WordParamsType:
        """Get Word study initial params."""
        return self._repo.fetch_initial(user)

    @override
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update Word study initial params."""
        return self._repo.update_initial(user, data)
