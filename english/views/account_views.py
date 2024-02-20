from django.db.models import F, Q
from django_filters.views import FilterView

from contrib_app.mixins import (
    CheckUserPkForOwnershipAccountMixin,
)
from english.models import WordModel


class UsersWordsView(
    CheckUserPkForOwnershipAccountMixin,
    FilterView,
):
    """Users word list view."""

    template_name = 'english/user_word_list_sql.html'
    model = WordModel
    context_object_name = 'words'

    def get_queryset(self):
        queryset = super(UsersWordsView, self).get_queryset(
        ).select_related(
            'source',
        ).prefetch_related(
            'knowledge_assessment',
            'favorites',
        ).filter(
            # !!!!! выведет значение любого пользователя
            pk=F('worduserknowledgerelation__word_id')
        ).annotate(
            assessment=F('worduserknowledgerelation__knowledge_assessment')
        ).annotate(
            favorite=Q(
                pk=F('wordsfavoritesmodel__word_id')
            ) & Q(
                user=F('wordsfavoritesmodel__user_id')
            )
        )
        return queryset

    extra_context = {
        'title': 'Мной изучаемые слова',
    }
