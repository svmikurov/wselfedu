"""Translation filters."""

from datetime import timedelta
from decimal import Decimal

import django_filters
from django.db.models import QuerySet
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.core import models as core_models

from .. import models


class TranslationFilter(django_filters.FilterSet):
    """Translation filter."""

    category = django_filters.ModelChoiceFilter(
        queryset=models.Category.objects.all(),
        empty_label=_('All categories'),
        label=_('Category'),
    )
    source = django_filters.ModelChoiceFilter(
        queryset=core_models.Source.objects.all(),
        empty_label=_('All sources'),
        label=_('Source'),
    )

    days = django_filters.NumberFilter(
        field_name=_('Date'),
        method='get_past_n_days',
        label=_('Past n days'),
    )

    class Meta:
        """Filter configuration."""

        model = models.EnglishTranslation
        fields = ['category', 'source', 'days']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Configure the filter."""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        if user:
            self.filters[  # type: ignore[attr-defined]
                'category'
            ].queryset = models.Category.objects.filter(user=user)  # type: ignore[misc]
            self.filters[  # type: ignore[attr-defined]
                'source'
            ].queryset = core_models.Source.objects.filter(user=user)  # type: ignore[misc]

    def get_past_n_days(
        self,
        queryset: QuerySet[models.EnglishTranslation],
        field_name: str,
        value: Decimal,
    ) -> QuerySet[models.EnglishTranslation]:
        """Filter by past n days."""
        time_threshold = timezone.now() - timedelta(days=int(value))
        return queryset.filter(created_at__gte=time_threshold)
