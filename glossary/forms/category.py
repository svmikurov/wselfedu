"""Glossary term category form."""

from django import forms

from glossary.models import GlossaryCategory


class CategoryForm(forms.ModelForm):
    """Glossary term category form."""

    class Meta:
        """Set up the form."""

        model = GlossaryCategory
        fields = ('name',)
