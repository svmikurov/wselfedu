"""Source form module."""

from django.forms import ModelForm

from foreign.models import WordSource


class SourceForm(ModelForm):
    """Source form class."""

    class Meta:
        """Add model with specific fields."""

        model = WordSource
        fields = ('name', 'url')
