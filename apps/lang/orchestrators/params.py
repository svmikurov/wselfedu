"""Abstract base class for Word study params orchestrator."""

from apps.lang import models
from apps.lang.orchestrators.abc import WordStudyParamsOrchestratorABC
from apps.lang.types import WordParamsType
from apps.users.models import CustomUser


class WordStudyParamsOrchestrator(WordStudyParamsOrchestratorABC):
    """ABC for Word study params orchestrator."""

    def fetch_initial(self, user: CustomUser) -> WordParamsType:
        """Fetch initial params."""
        labels = models.LangLabel.objects.filter(user=user).values(
            'id', 'name'
        )
        categories = models.LangCategory.objects.filter(user=user).values(
            'id', 'name'
        )
        return {
            'user_id': user.pk,
            'categories': list(categories),
            'labels': list(labels),
        }
