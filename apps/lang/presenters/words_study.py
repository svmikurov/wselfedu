"""Word study presenter."""

from typing import override

from ..types import WordParamsType, WordType
from .abc import WordStudyPresenterABC


class WordStudyPresenter(WordStudyPresenterABC):
    """Presenter for Word study exercise."""

    @override
    def get_presentation(self, params: WordParamsType) -> WordType:
        """Get Word study presentation case."""
        return {
            'definition': 'слово для перевода',
            'explanation': 'перевод слова',
        }
