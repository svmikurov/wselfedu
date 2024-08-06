"""Category form module."""

from django.forms import ModelForm

from english.models import CategoryModel


class CategoryForm(ModelForm):
    """Category form class."""

    class Meta:
        """Add model with specific fields."""

        model = CategoryModel
        fields = ('name',)
