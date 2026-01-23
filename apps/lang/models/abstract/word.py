"""Word model."""

from apps.core.models import AbstractBaseModel

__all__ = [
    'AbstractWordModel',
]


class AbstractWordModel(AbstractBaseModel):
    """Base word model."""

    WORD_LENGTH = 70

    class Meta:
        """Model configuration."""

        abstract = True

    def __str__(self) -> str:
        """Get string representation."""
        return str(self.word)
