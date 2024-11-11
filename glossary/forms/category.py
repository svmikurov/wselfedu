"""Term term category form."""

from django import forms

from glossary.models import TermCategory


class CategoryForm(forms.ModelForm):
    """Term term category form."""

    class Meta:
        """Set up the form."""

        model = TermCategory
        fields = ('name',)
