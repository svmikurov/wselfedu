"""Word study params repository."""

from typing import override

from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch_initial(self, user: CustomUser) -> types.ParamsChoicesT:
        """Fetch initial params."""
        parameters = models.Params.objects.filter(user=user)
        categories = models.LangCategory.objects.filter(user=user)
        labels = models.LangLabel.objects.filter(user=user)

        data = {
            # Choices
            'categories': list(categories.values('id', 'name')),
            'labels': list(labels.values('id', 'name')),
            # Initial parameters
            'category': None,
            'label': None,
        }

        initial_data = parameters.values(
            'category__id',
            'category__name',
            'label__id',
            'label__name',
        ).first()

        if not initial_data:
            return data  # type: ignore[return-value]

        if initial_data.get('category__id'):
            data['category'] = {  # type: ignore[assignment]
                'id': initial_data['category__id'],
                'name': initial_data['category__name'],
            }
        if initial_data.get('label__id'):
            data['label'] = {  # type: ignore[assignment]
                'id': initial_data['label__id'],
                'name': initial_data['label__name'],
            }

        return data  # type: ignore[return-value]

    @override
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update initial params."""
