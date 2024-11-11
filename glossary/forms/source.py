"""Glossary term source form."""

from django import forms

from glossary.models import TermSource


class SourceForm(forms.ModelForm):
    """Glossary term source form."""

    class Meta:
        """Set up the form."""

        model = TermSource
        fields = ('name', 'url')
