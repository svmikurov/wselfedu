"""Word study params presenter."""

from typing import override

from ..types import WordParamsType
from .abc import (
    WordStudyParamsPresenterABC,
)


class WordStudyParamsPresenter(WordStudyParamsPresenterABC):
    """Word study params presenter."""

    @override
    def get_initial(self) -> WordParamsType:
        """Get Word study initial params."""
        return {
            'category': [],
            'marks': [],
            'user_id': 1,
        }
