"""Source form module."""

from django.forms import ModelForm

from config.constants import NAME, URL
from english.models import SourceModel


class SourceForm(ModelForm):
    """Source form class."""

    class Meta:
        """Add model with specific fields."""

        model = SourceModel
        fields = (NAME, URL)
