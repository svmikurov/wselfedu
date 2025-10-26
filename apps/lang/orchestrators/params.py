"""Abstract base class for Word study params orchestrator."""

from apps.lang.orchestrators.abc import WordStudyParamsOrchestratorABC
from apps.lang.types import WordParamsType
from apps.users.models import CustomUser


class WordStudyParamsOrchestrator(WordStudyParamsOrchestratorABC):
    """ABC for Word study params orchestrator."""

    def fetch_initial(self, user: CustomUser) -> WordParamsType:
        """Fetch initial params."""
        return {
            'category': [],
            'marks': [],
            'user_id': 1,
        }
