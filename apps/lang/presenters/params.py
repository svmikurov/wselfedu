"""Word study params presenter."""

from typing import override

from apps.users.models import CustomUser

from ..repositories.abc import WordStudyParamsRepositoryABC
from ..types import WordParamsType
from .abc import (
    WordStudyParamsPresenterABC,
)


class WordStudyParamsPresenter(WordStudyParamsPresenterABC):
    """Word study params presenter."""

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
