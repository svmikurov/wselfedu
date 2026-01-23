"""Language discipline category model."""

from django.utils.translation import gettext as _

from apps.core.models.abstract.category import AbstractCategory

__all__ = [
    'Category',
]


class Category(AbstractCategory):
    """Language discipline category."""

    class Meta:
        """Model configuration."""

        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
