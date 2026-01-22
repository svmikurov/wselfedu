"""Translation filters."""

import django_filters

from apps.core import models as core_models

from .. import models


class TranslationFilter(django_filters.FilterSet):
    """Translation filter."""

    category = django_filters.ModelChoiceFilter(
        queryset=models.Category.objects.all(),
        empty_label='Все категории',
        label='Категория',
    )
    source = django_filters.ModelChoiceFilter(
        queryset=core_models.Source.objects.all(),
        empty_label='Все источники',
        label='Источник',
    )

    class Meta:
        """Filter configuration."""

        model = models.EnglishTranslation
        fields = ['category', 'source']

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
