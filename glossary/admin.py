from django import forms
from django.contrib import admin

from glossary.models import Glossary, GlossaryCategory


@admin.register(Glossary)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ['term', 'definition']
    exclude = ['created_at']

    def get_form(self, request, obj=None, **kwargs):
        """Set Textarea widget for ``definition`` field."""
        kwargs['widgets'] = {
            'definition': forms.Textarea,
        }
        return super().get_form(request, obj, **kwargs)


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    exclude = ['created_at']
