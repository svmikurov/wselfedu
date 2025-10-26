"""Word study params presenter."""

from typing import override

from .abc import (
    WordStudyInitialParamsType,
    WordStudyParamsPresenterABC,
)


class WordStudyParamsPresenter(WordStudyParamsPresenterABC):
    """Word study params presenter."""

    @override
    def get_initial(self) -> WordStudyInitialParamsType:
        """Get Word study initial params."""
        return {'marks': []}
