"""User word list view module."""

from django.db.models import F, Q
from django.db.models.query import QuerySet
from django_filters.views import FilterView

from config.constants import PK, PROGRESS, SOURCE, TITLE, WORDS
from contrib.views import CheckObjectOwnershipMixin
from foreign.models import Word


class UserWordListView(
    CheckObjectOwnershipMixin,
    FilterView,
):
    """Users word list view."""

    template_name = 'foreign/user_word_list.html'
    model = Word
    context_object_name = WORDS
    extra_context = {
        TITLE: 'Изучаемые слова',
    }

    def get_queryset(self) -> QuerySet:
        """Get user word list with relations."""
        user = self.request.user
        user_favorites = Word.objects.filter(
            wordfavorites__word_id=F(PK),
            wordfavorites__user_id=user,
        ).values(PK)

        queryset = (
            super()
            .get_queryset()
            .select_related(SOURCE)
            .prefetch_related(PROGRESS)
            .filter(user=user)
            # `wordprogress__user_id__isnull=True`
            # allows to a create query using LEFT JOIN
            .filter(
                Q(wordprogress__user_id__isnull=True)
                | Q(wordprogress__user_id=user.pk)
            )
            .annotate(assessment=F('wordprogress__progress'))
            # if `favorite` is `True` then word is favorites
            .annotate(favorite=Q(pk__in=user_favorites))
        )

        return queryset
