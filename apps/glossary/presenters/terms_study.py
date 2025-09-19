"""Terms study presenter."""

from ..types import ParamsType, QuestionType


class TermsStudyPresenter:
    """Presenter for Terms study exercise."""

    def get_question(self, params: ParamsType) -> QuestionType:
        """Get Ters study exercise question."""
        return {
            'term': 'термин',
            'definition': 'определение термина',
        }
