"""English language form fields."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django import forms

from .. import models
from . import queries

if TYPE_CHECKING:
    from apps.users.models import Person


def create_clause_field(user: Person, pk: int) -> forms.ModelChoiceField:  # type: ignore[type-arg]
    """Create clause field."""
    return forms.ModelChoiceField(
        queryset=queries.get_clauses_qs(user, pk),
        label='Пункт правила',
    )


def create_example_type_field() -> forms.ChoiceField:
    """Create example type field."""
    return forms.ChoiceField(
        choices=models.ExampleType,
        label='Пример / Исключение',
    )


def create_source_field(user: Person) -> forms.ModelChoiceField:  # type: ignore[type-arg]
    """Create source field."""
    return forms.ModelChoiceField(
        queryset=queries.get_source_qs(user),
        label='Источник',
        required=False,
    )


def create_marks_field(user: Person) -> forms.ModelMultipleChoiceField:  # type: ignore[type-arg]
    """Create marks field."""
    return forms.ModelMultipleChoiceField(
        queryset=queries.get_marks_qs(user),
        label='Маркер примера',
        required=False,
    )


def create_translation_choices(
    user: Person,
) -> forms.MultipleChoiceField:
    """Create marks field."""
    translation_choices = queries.get_translations(user)
    return forms.MultipleChoiceField(
        choices=list(translation_choices),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Выберите элементы',
    )
