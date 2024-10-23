"""Representation of models in the admin interface module."""

from typing import Optional

from django import forms
from django.contrib import admin
from django.forms import Form
from django.http import HttpRequest

from config.constants import (
    CATEGORY,
    CREATED_AT,
    DEFINITION,
    ID,
    NAME,
    TERM,
    USER,
)
from glossary.models import (
    Glossary,
    GlossaryCategory,
    GlossaryParams,
)


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = [TERM, DEFINITION, CATEGORY, USER]
    exclude = [CREATED_AT]

    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[object] = None,
        **kwargs: object,
    ) -> Form:
        """Set Textarea widget for ``definition`` field."""
        kwargs['widgets'] = {
            DEFINITION: forms.Textarea,
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = [ID, USER, NAME]
    exclude = [CREATED_AT]


@admin.register(GlossaryParams)
class GlossaryExerciseSettingsAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""
