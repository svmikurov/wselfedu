"""Category abstract model."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from .base import AbstractBaseModel


class AbstractCategory(AbstractBaseModel):
    """Category abstract model."""

    CATEGORY_NAME_LENGTH = 70

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    name = models.CharField(
        max_length=CATEGORY_NAME_LENGTH,
        unique=True,
        verbose_name=_('Category'),
    )

    class Meta:
        """Model configuration."""

        abstract = True

    def __str__(self) -> str:
        """Get string representation."""
        return self.name
