"""Term detail presenter."""

from django.db.models import Prefetch
from django.db.models.query import QuerySet

from apps.users.models import Person

from ..models import Term, TermAssertion


class TermDetailPresenter:
    """Presenter for term detail."""

    @staticmethod
    def get_term(user: Person) -> QuerySet[Term]:
        """Get detail term."""
        # fmt: off
        return (
            Term.objects
            .filter(user=user)
            .prefetch_related(
                Prefetch(
                    'assertions',
                    queryset=(
                        TermAssertion.objects
                        .only('assertion', 'created_at')
                        .order_by('created_at')
                    ),
                    to_attr='sorted_assertions',
                )
            )
        )

    # fmt: on
