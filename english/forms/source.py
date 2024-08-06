"""Source form module."""

from django.forms import ModelForm

from english.models import SourceModel


class SourceForm(ModelForm):
    """Source form class."""

    class Meta:
        """Add model with specific fields."""

        model = SourceModel
        fields = ('name', 'url')
