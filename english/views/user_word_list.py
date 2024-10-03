"""User word list view module."""

from django.db.models import F, Q
from django.db.models.query import QuerySet
from django_filters.views import FilterView

from config.constants import PK, PROGRESS, SOURCE, TITLE, WORDS
from contrib.mixins_views import CheckObjectOwnershipMixin
from english.models import WordModel


class UserWordListView(
    CheckObjectOwnershipMixin,
    FilterView,
):
    """Users word list view."""

    template_name = 'foreign/user_word_list.html'
    model = WordModel
    context_object_name = WORDS
    extra_context = {
        TITLE: 'Изучаемые слова',
    }

    def get_queryset(self) -> QuerySet:
        """Get user word list with relations."""
        user = self.request.user
        user_favorites = WordModel.objects.filter(
            wordsfavoritesmodel__word_id=F(PK),
            wordsfavoritesmodel__user_id=user,
        ).values(PK)

        queryset = (
            super()
            .get_queryset()
            .select_related(SOURCE)
            .prefetch_related(PROGRESS)
            .filter(user=user)
            # `worduserknowledgerelation__user_id__isnull=True`
            # allows to a create query using LEFT JOIN
            .filter(
                Q(worduserknowledgerelation__user_id__isnull=True)
                | Q(worduserknowledgerelation__user_id=user.pk)
            )
            .annotate(assessment=F('worduserknowledgerelation__progress'))
            # if `favorite` is `True` then word is favorites
            .annotate(favorite=Q(pk__in=user_favorites))
        )

        return queryset
