"""Form queries."""

from __future__ import annotations

from typing import TYPE_CHECKING

from apps.core import models as core_models

from .. import models

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person


def get_source_qs(user: Person) -> QuerySet[core_models.Source]:
    """Get the user's source queryset."""
    return core_models.Source.objects.filter(user=user)


def get_marks_qs(user: Person) -> QuerySet[models.LangMark]:
    """Get the user's marks queryset."""
    return models.LangMark.objects.filter(user=user)


def get_clauses_qs(user: Person, pk: int) -> QuerySet[models.RuleClause]:
    """Get the user's rule clauses queryset."""
    return models.RuleClause.objects.filter(rule=pk, user=user)


def get_foreign(user: Person, word: str) -> models.EnglishWord:
    """Get the users's foreign word object.

    Gets or creates English word object.
    """
    obj, _ = models.EnglishWord.objects.get_or_create(user=user, word=word)
    return obj


def get_native(user: Person, word: str) -> models.NativeWord:
    """Get the users's foreign word object.

    Gets or creates Native word object.
    """
    obj, _ = models.NativeWord.objects.get_or_create(user=user, word=word)
    return obj
