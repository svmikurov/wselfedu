"""Category form."""

from apps.core.forms import BaseNameForm

from ..models import Category


class CategoryForm(BaseNameForm[Category]):
    """Category form."""

    class Meta:
        """Form configuration."""

        model = Category
        fields = ['name']
