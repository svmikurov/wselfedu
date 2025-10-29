"""Abstract base class for Word study params orchestrator."""

from apps.lang import models
from apps.lang.orchestrators.abc import WordStudyParamsOrchestratorABC
from apps.lang.types import DefaultWordParamsType, WordParamsType
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
        default_query = (
            models.Params.objects.filter(user=user)  # type: ignore[var-annotated]
            .values(
                'category__id',
                'category__name',
                'label__id',
                'label__name',
                'word_count',
            )
            .first()
            or {}
        )

        default: DefaultWordParamsType = {
            'category': {
                'id': default_query['category__id'],
                'name': default_query['category__name'],
            }
            if default_query.get('category__id')
            else None,
            'label': {
                'id': default_query['label__id'],
                'name': default_query['label__name'],
            }
            if default_query.get('label__id')
            else None,
            'word_count': default_query.get('word_count'),
        }

        return {
            'user_id': user.pk,
            'categories': list(categories),
            'labels': list(labels),
            'default': default,
        }
