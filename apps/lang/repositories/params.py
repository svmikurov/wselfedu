"""Abstract base class for Word study params repository."""

from apps.lang import models
from apps.lang.repositories.abc import WordStudyParamsRepositoryABC
from apps.lang.types import WordCaseParamsType, WordParamsType
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """ABC for Word study params repository."""

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

        default_params: WordCaseParamsType = {
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
            'categories': list(categories),
            'labels': list(labels),
            'default_params': default_params,
        }
