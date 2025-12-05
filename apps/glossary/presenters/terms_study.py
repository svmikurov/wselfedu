"""Terms study presenter."""

from apps.users.models import Person

from ..types import TermParamsType, TermType
from .abc import TermStudyPresenterABC


class TermStudyPresenter(TermStudyPresenterABC):
    """Presenter for Terms study exercise."""

    def get_presentation_case(
        self,
        user: Person,
        params: TermParamsType,
    ) -> TermType:
        """Get Term study presentation case."""
        return {
            'term': 'термин',
            'definition': 'определение термина',
        }
