"""Word study params repository."""

from typing import override

from django.db import transaction

from apps.core import models as core_models
from apps.lang import models, types
from apps.lang.repos.abc import WordStudyParamsRepositoryABC
from apps.users.models import CustomUser


class WordStudyParamsRepository(WordStudyParamsRepositoryABC):
    """Word study params repository."""

    @override
    def fetch(self, user: CustomUser) -> types.WordPresentationParamsT:
        """Fetch parameters with parameter choices."""
        # TODO: Fix database query (N+1)? Now 4.
        parameters = models.Params.objects.filter(user=user)
        categories = models.LangCategory.objects.filter(user=user)
        marks = models.LangMark.objects.filter(user=user)
        sources = core_models.Source.objects.filter(user=user)

        data = {
            # Parameter choices
            'categories': list(categories.values('id', 'name')),
            'marks': list(marks.values('id', 'name')),
            'sources': list(sources.values('id', 'name')),
            # Initial parameters
            'category': None,
            'mark': None,
            'word_source': None,
        }

        initial = parameters.values(
            'category__id',
            'category__name',
            'mark__id',
            'mark__name',
            'word_source__id',
            'word_source__name',
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
        if initial.get('word_source__id'):
            data['word_source'] = {  # type: ignore[assignment]
                'id': initial['word_source__id'],
                'name': initial['word_source__name'],
            }

        return data  # type: ignore[return-value]

    @override
    @transaction.atomic
    def update(
        self,
        user: CustomUser,
        data: types.UpdateParametersT,
    ) -> types.WordPresentationParamsT:
        """Update initial parameters."""
        (
            models.Params.objects.select_for_update()
            .filter(user=user)
            .update(
                category=data['category']['id'],  # type: ignore[index]
                mark=data['mark']['id'],  # type: ignore[index]
                word_source=data['word_source']['id'],  # type: ignore[index]
            )
        )
        return self.fetch(user)
