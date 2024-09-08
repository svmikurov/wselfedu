"""Representation of models in the admin interface module."""

from typing import Optional

from django import forms
from django.contrib import admin
from django.forms import Form
from django.http import HttpRequest

from glossary.models import (
    Glossary,
    GlossaryCategory,
    GlossaryExerciseParams,
)


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = ['term', 'definition', 'category']
    exclude = ['created_at']

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


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    exclude = ['created_at']


@admin.register(GlossaryExerciseParams)
class GlossaryExerciseSettingsAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""
