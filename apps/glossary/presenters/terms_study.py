"""Terms study presenter."""

from ..types import TermParamsType, TermType


class TermStudyPresenter:
    """Presenter for Terms study exercise."""

    def get_presentation(self, params: TermParamsType) -> TermType:
        """Get Ters study exercise question."""
        return {
            'term': 'термин',
            'definition': 'определение термина',
        }
