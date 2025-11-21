"""Word study params repository."""

from typing import override

from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: CustomUser) -> types.WordPresentationParamsT:
        """Fetch parameters with parameter choices."""
        parameters = models.Params.objects.filter(user=user)
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)

        data = {
            # Parameter choices
            'categories': list(categories.values('id', 'name')),
            'marks': list(marks.values('id', 'name')),
            # Initial parameters
            'category': None,
            'mark': None,
        }

        initial = parameters.values(
            'category__id',
            'category__name',
            'mark__id',
            'mark__name',
        ).first()

        if not initial:
            return data  # type: ignore[return-value]

        if initial.get('category__id'):
            data['category'] = {  # type: ignore[assignment]
                'id': initial['category__id'],
                'name': initial['category__name'],
            }
        if initial.get('mark__id'):
            data['mark'] = {  # type: ignore[assignment]
                'id': initial['mark__id'],
                'name': initial['mark__name'],
            }

        return data  # type: ignore[return-value]

    @override
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update initial params."""
