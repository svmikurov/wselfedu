"""Abstract base class for Word study params repository."""

from typing import override

from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """ABC for Word study params repository."""

    @override
    def fetch_initial(self, user: CustomUser) -> types.ParamsChoicesT:
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

        initial_choices: types.InitialChoicesT = {
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
            # TODO: Add database tables for choices
            'word_source': None,
            'order': None,
            'start_period': None,
            'end_period': None,
        }

        # TODO: Fix type ignore
        return {  # type: ignore[typeddict-unknown-key]
            'categories': list(categories),
            'labels': list(labels),
            'category': initial_choices['category'],
            'label': initial_choices['label'],
        }

    @override
    def update_initial(self, user: CustomUser, data: object) -> None:
        """Update initial params."""
        pass
