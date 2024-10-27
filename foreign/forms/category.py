"""Category form module."""

from django.forms import ModelForm

from foreign.models import WordCategory


class CategoryForm(ModelForm):
    """Category form class."""

    class Meta:
        """Add model with specific fields."""

        model = WordCategory
        fields = ('name',)
