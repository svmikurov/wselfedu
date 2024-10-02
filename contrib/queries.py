"""General ORM queries."""

from django.db.models import Q


def get_q(lookup_field: str, lookup_value: object) -> Q:
    """Get SQL condition representation."""
    return Q(**{lookup_field: lookup_value}) if lookup_value else Q()
