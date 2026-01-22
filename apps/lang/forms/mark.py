"""Mark form."""

from apps.core.forms import BaseNameForm

from ..models import Mark


class MarkForm(BaseNameForm[Mark]):
    """Mark form."""

    class Meta:
        """Form configuration."""

        model = Mark
        fields = ['name']
