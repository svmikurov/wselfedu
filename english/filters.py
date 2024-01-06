import django_filters

from english.models import (
    CategoryModel,
    SourceModel,
    WordModel, WordUserKnowledgeRelation,
)
from users.models import UserModel


class WordsFilter(django_filters.FilterSet):
    """Words filter"""

    WORD_COUNT = (
        ('OW', 'Слово'),
        ('CB', 'Словосочетание'),
        ('PS', 'Часть предложения'),
        ('ST', 'Предложение'),
        ('NC', 'Не указано'),
    )

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
    filtered_word_count = django_filters.ChoiceFilter(
        choices=WORD_COUNT,
        lookup_expr='icontains',
        field_name='word_count',
        label='',
        empty_label='Любое кол-во слов',
    )
    # filtered_knowledge_assessment = django_filters.ChoiceFilter(
    #     field_name='knowledge_assessment',
    #     method='get_knowledge_assessment_by_user',
    #     label='',
    #     empty_label='Оценка',
    # )
    #
    # def get_knowledge_assessment_by_user(self, request, *args, **kwargs):
    #     """Получи список оценок знания слов текущего пользователя."""
    #     queryset = WordUserKnowledgeRelation.objects.filter(
    #         user=UserModel.objects.get(pk=request.user.pk),
    #     )
    #     return queryset
