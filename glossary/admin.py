"""Representation of models in the admin interface module."""

from typing import Optional

from django import forms
from django.contrib import admin
from django.forms import Form
from django.http import HttpRequest

from glossary.models import (
    GlossaryParams,
    Term,
    TermCategory,
)


@admin.register(Term)
class GlossaryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = [
        'term',
        'progress',
        'definition',
        'category',
        'user',
    ]

    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[object] = None,
        **kwargs: object,
    ) -> Form:
        """Set Textarea widget for ``definition`` field."""
        kwargs['widgets'] = {
            'definition': forms.Textarea,
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(TermCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = ['id', 'user', 'name']
    exclude = ['created_at']


@admin.register(GlossaryParams)
class GlossaryExerciseSettingsAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = [
        'user',
        'category',
        'source',
        'timeout',
        'favorites',
        'progress',
        'period_start_date',
        'period_end_date',
        'count_first',
        'count_last',
    ]
