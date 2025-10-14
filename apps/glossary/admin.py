"""Glossary app model management."""

from django.contrib import admin

from .models import Term, TermAssertion


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Term model administration."""

    list_display = ['user', 'name', 'definition']


@admin.register(TermAssertion)
class AssertionModel(admin.ModelAdmin):  # type: ignore[type-arg]
    """Term assertion model administration."""

    list_display = ['term', 'assertion']
