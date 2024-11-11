"""Term term source form."""

from django import forms

from glossary.models import TermSource


class SourceForm(forms.ModelForm):
    """Term term source form."""

    class Meta:
        """Set up the form."""

        model = TermSource
        fields = ('name', 'url')
