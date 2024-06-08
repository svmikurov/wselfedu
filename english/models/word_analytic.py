from django.db import models

from english.models import WordModel


class WordLearningStories(models.Model):
    """Word learning stories model.

    Stores information about the user's word learning.
    Related to :model:`english.WordModel`
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

    @classmethod
    def add_display_fact(cls, word_id):
        """Add a display fact to the display statics."""
        even = cls(word_id=word_id)
        print(f'{even = }')
        # even.update(display_count=F('display_count') + 1)
        # return even
