"""Test data collection for analytical purposes.

Data is collected from the “Learning words” exercise.
"""

from django.urls import reverse_lazy

from config.constants import (
    TO_NATIVE,
)
from contrib.tests_extension import UserAuthTestCase
from foreign.models import Word, WordAnalytics


class TestCollectData(UserAuthTestCase):
    """Testing data collection from a Word Study exercise."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data.

        Add page path schema and word to dictionary.
        """
        super().setUpTestData()
        cls.url = reverse_lazy('foreign:foreign_translate_demo')
        Word.objects.create(
            foreign_word='word',
            user=cls.user,
        )

    def test_collect_number_word_displays(self) -> None:
        """Test collect the number of word displays."""
        task_conditions = {'timeout': 1, 'language_order': TO_NATIVE}
        self.set_session(**{'task_conditions': task_conditions})
        self.get_auth_response(self.url, method='post')

        self.assertEqual(
            WordAnalytics.objects.get(pk=1).display_count,
            1,
        )
