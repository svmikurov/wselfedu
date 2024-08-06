"""Representation of models in the admin interface module."""

from django import forms
from django.contrib import admin

from glossary.models import Glossary, GlossaryCategory


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = ['term', 'definition', 'category']
    exclude = ['created_at']

    def get_form(self, request, obj=None, **kwargs):
        """Set Textarea widget for ``definition`` field."""
        kwargs['widgets'] = {
            'definition': forms.Textarea,
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    exclude = ['created_at']
