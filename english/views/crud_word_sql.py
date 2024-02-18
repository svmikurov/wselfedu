from django_filters.views import FilterView

from english.models import WordModel

PAGINATE_NUMBER = 20
DEFAULT_CATEGORY = 'Developer'
"""Константа значения добавления категории по умолчанию, если пользователем не
не указана категория.
"""


class SqlShowUserWordsView(FilterView):
    """View user word list page, via ROW SQL queries."""

    model = WordModel
    template_name = 'english/user_word_list.html'
    paginate_by = PAGINATE_NUMBER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        words = WordModel.objects.all().select_related(
            'user',
            'source',
            'category',
            'lesson',
        )
        context['words'] = words
        return context
