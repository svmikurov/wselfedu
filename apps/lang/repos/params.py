"""Word study params repository."""

from typing import override

from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: CustomUser) -> types.ParamsChoicesT:
        """Fetch parameters with parameter choices."""
        parameters = models.Params.objects.filter(user=user)
        categories = models.LangCategory.objects.filter(user=user)
        labels = models.LangLabel.objects.filter(user=user)

        data = {
            # Parameter choices
            'categories': list(categories.values('id', 'name')),
            'labels': list(labels.values('id', 'name')),
            # Initial parameters
            'category': None,
            'label': None,
        }

        initial = parameters.values(
            'category__id',
            'category__name',
            'label__id',
            'label__name',
        ).first()

        if not initial:
            return data  # type: ignore[return-value]

        if initial.get('category__id'):
            data['category'] = {  # type: ignore[assignment]
                'id': initial['category__id'],
                'name': initial['category__name'],
            }
        if initial.get('label__id'):
            data['label'] = {  # type: ignore[assignment]
                'id': initial['label__id'],
                'name': initial['label__name'],
            }

        return data  # type: ignore[return-value]

    @override
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update initial params."""
