from django.db import models

from english.models import WordModel


class WordLearningStories(models.Model):
    """Word learning stories model.

    Stores information about the user's word learning.
    Related to `english.WordModel`

    Attributes
    ----------
    word : `OneToOneField`
        Word id, relate ``WordModel``.
    display_count : `PositiveSmallIntegerField`
        The count of displaying specific word to user.
    """

    word = models.OneToOneField(
        WordModel,
        on_delete=models.CASCADE,
        related_name='stories',
        help_text='ID of the word being studied.',
    )
    display_count = models.PositiveSmallIntegerField(
        default=0,
        help_text='The number of times the word was displayed to the user.'
    )

    def __str__(self):
        """Represent an instance as a string."""
        return self.word
