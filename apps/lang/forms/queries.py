"""Form queries."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import Exists, OuterRef, Value
from django.db.models.functions import Concat

from apps.core import models as core_models

from .. import models

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person


def get_source_qs(user: Person) -> QuerySet[core_models.Source]:
    """Get the user's source queryset."""
    return core_models.Source.objects.filter(user=user)


def get_marks_qs(user: Person) -> QuerySet[models.Mark]:
    """Get the user's marks queryset."""
    return models.Mark.objects.filter(user=user)


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


def get_translations(user: Person) -> QuerySet[models.EnglishTranslation, Any]:
    """Get user translations."""
    return models.EnglishTranslation.objects.filter(user=user).annotate(
        display_name=Concat(
            'foreign__word',
            Value(' - '),
            'native__word',
        )
    )


def get_exercise_translations(
    user: Person,
    exercise_id: int | None = None,
) -> QuerySet[models.EnglishTranslation, Any]:
    """Get user translations."""
    translations = get_translations(user)

    if exercise_id:
        subquery = models.EnglishExerciseTranslation.objects.filter(
            exercise=exercise_id,
            translation=OuterRef('pk'),
        )
        return translations.annotate(
            is_active=Exists(subquery),
        )

    return translations


def get_exercises(
    user: Person,
) -> QuerySet[models.LangExercise]:
    """Get mentor exercises."""
    return models.LangExercise.objects.filter(
        user=user,
    )


def get_assignations(
    user: Person,
) -> QuerySet[models.EnglishAssignedExercise]:
    """Get mentor assigned exercises."""
    return models.EnglishAssignedExercise.objects.filter(
        mentorship__mentor=user,
    )
