"""Term exercise lookup parameters to database query."""

from django.db.models import Q

from contrib.lookup_params import LookupParams


class TermLookupParams(LookupParams):
    """Term exercise lookup parameters to database query.

    To get lookup parameters of class instance, use property ``params``.

    The term lookup parameters to database query for glossary exercise.
    Filters the terms by user conditions to study terms.

    :param dict[str, str | int] lookup_conditions: Lookup conditions of
     term query for Term exercise.
    """

    def __init__(self, lookup_conditions: dict) -> None:
        """Set lookup conditions."""
        super().__init__(lookup_conditions)

    @property
    def params(self) -> tuple[Q, ...]:
        """Exercise lookup params (tuple[Q, ...], read-only)."""
        return (
            self.user,
            self.period_start_date,
            self.period_end_date,
            self.category,
            self.progress,
        )
