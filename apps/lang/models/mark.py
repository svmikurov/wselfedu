"""Language discipline mark models."""

from django.db import models
from django.utils.translation import gettext as _

from apps.core.models import AbstractBaseModel
from apps.core.models.abstract.mark import AbstractMark

__all__ = [
    'Mark',
    'TranslationMark',
]


class Mark(AbstractMark):
    """Language discipline mark."""

    class Meta:
        """Model configuration."""

        verbose_name = _('Mark')
        verbose_name_plural = _('Marks')


class TranslationMark(AbstractBaseModel):
    """English translation mark."""

    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name=_('Translation'),
    )
    mark = models.ForeignKey(
        'Mark',
        on_delete=models.CASCADE,
        verbose_name=_('Mark'),
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Маркировка перевода'
        verbose_name_plural = 'Маркировки переводов'

        unique_together = ['translation', 'mark']

        db_table = 'lang_translation_mark'
