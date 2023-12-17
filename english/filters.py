import django_filters

from english.models import (
    CategoryModel,
    SourceModel,
)


class WordsFilter(django_filters.FilterSet):
    filtered_category = django_filters.ModelChoiceFilter(
        queryset=CategoryModel.objects.all(),
        field_name='category',
        lookup_expr='exact',
        label='',
        empty_label='Категория',
    )
    filtered_source = django_filters.ModelChoiceFilter(
        queryset=SourceModel.objects.all(),
        field_name='source',
        lookup_expr='exact',
        label='',
        empty_label='Источник',
    )
