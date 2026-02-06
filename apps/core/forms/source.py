"""Source form."""

from ..models import Source
from . import BaseNameForm


class SourceForm(BaseNameForm[Source]):
    """Source form."""

    class Meta:
        """Form configuration."""

        model = Source
        fields = ['name']
