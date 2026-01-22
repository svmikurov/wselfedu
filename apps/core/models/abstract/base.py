"""Base abstract model."""

from django.db import models
from django.utils.translation import gettext as _


class AbstractBaseModel(models.Model):
    """Base abstract model."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    class Meta:
        """Model configuration."""

        abstract = True
