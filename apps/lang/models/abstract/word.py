"""Word model."""

from django.db import models

from apps.core.models import AbstractBaseModel

__all__ = [
    'AbstractWordModel',
]


class AbstractWordModel(AbstractBaseModel):
    """Base word model."""

    WORD_LENGTH = 70

    word = models.CharField(max_length=WORD_LENGTH)

    class Meta:
        """Model configuration."""

        abstract = True

    def __str__(self) -> str:
        """Get string representation."""
        return str(self.word)
