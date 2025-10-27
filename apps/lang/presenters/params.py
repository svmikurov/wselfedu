"""Word study params presenter."""

from typing import override

from apps.users.models import CustomUser

from ..orchestrators.abc import WordStudyParamsOrchestratorABC
from ..types import WordParamsType
from .abc import (
    WordStudyParamsPresenterABC,
)


class WordStudyParamsPresenter(WordStudyParamsPresenterABC):
    """Word study params presenter."""

    def __init__(
        self,
        orchestrator: WordStudyParamsOrchestratorABC,
    ) -> None:
        """Construct the presenter."""
        self.orchestrator = orchestrator

    @override
    def get_initial(self, user: CustomUser) -> WordParamsType:
        """Get Word study initial params."""
        return self.orchestrator.fetch_initial(user)
