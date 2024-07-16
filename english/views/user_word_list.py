from django.db.models import F, Q
from django_filters.views import FilterView

from contrib.mixins_views import CheckObjectOwnershipMixin
from english.models import WordModel


class UserWordListView(
    CheckObjectOwnershipMixin,
    FilterView,
):
    """Users word list view."""

    template_name = 'english/user_word_list.html'
    model = WordModel
    context_object_name = 'words'
    extra_context = {
        'title': 'Изучаемые слова',
    }

    def get_queryset(self):
        """Get user word list with relations.
        """
        user_favorites = WordModel.objects.filter(
            wordsfavoritesmodel__word_id=F('pk'),
            wordsfavoritesmodel__user_id=self.request.user
        ).values('pk')

        queryset = super().get_queryset(
        ).select_related(
            'source',
        ).prefetch_related(
            'knowledge_assessment',
        ).filter(
            user=self.request.user
        ).filter(
            # `worduserknowledgerelation__user_id__isnull=True` allows
            # to a create query using LEFT JOIN
            Q(worduserknowledgerelation__user_id__isnull=True)
            | Q(worduserknowledgerelation__user_id=self.request.user.pk)
        ).annotate(
            assessment=F('worduserknowledgerelation__knowledge_assessment'),
        ).annotate(
            # if `favorite` is `True` then word is favorites
            favorite=Q(pk__in=user_favorites)
        )

        return queryset
