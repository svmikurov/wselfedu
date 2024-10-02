"""Word learning stories module."""

from django.db import models

from config.constants import DISPLAY_COUNT
from foreign.models import Word


class WordAnalytics(models.Model):
    """Word learning stories model.

    Stores information about the user's word learning.
    """

    word = models.OneToOneField(
        Word,
        on_delete=models.CASCADE,
        related_name='stories',
        help_text='ID of the word being studied.',
    )
    """Word ID, relate ``WordModel``.
    """
    display_count = models.PositiveSmallIntegerField(
        default=0,
        help_text='The number of times the word was displayed to the user.',
    )
    """The count of displaying specific word to user.
    """

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.word

    class Meta:
        """Set model features."""

        verbose_name = 'История изучения слов'
        verbose_name_plural = 'История изучения слов'
        ordering = [DISPLAY_COUNT]
