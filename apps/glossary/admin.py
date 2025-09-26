"""Glossary app model management."""

from django.contrib import admin

from apps.glossary.models import Term


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Term model administration."""

    list_display = ['user', 'name', 'definition']
