"""Terms study presenter."""

from apps.users.models import CustomUser

from ..types import TermParamsType, TermType
from .abc import TermStudyPresenterABC


class TermStudyPresenter(TermStudyPresenterABC):
    """Presenter for Terms study exercise."""

    def get_presentation(
        self,
        params: TermParamsType,
        user: CustomUser,
    ) -> TermType:
        """Get Term study presentation case."""
        return {
            'term': 'термин',
            'definition': 'определение термина',
        }
