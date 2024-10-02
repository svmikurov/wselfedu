"""Source form module."""

from django.forms import ModelForm

from config.constants import NAME, URL
from foreign.models import WordSource


class SourceForm(ModelForm):
    """Source form class."""

    class Meta:
        """Add model with specific fields."""

        model = WordSource
        fields = (NAME, URL)
