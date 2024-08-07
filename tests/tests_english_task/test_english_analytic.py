"""Test data collection for analytical purposes.

Data is collected from the “Learning words” exercise.
"""

from django.urls import reverse_lazy

from contrib.tests_extension import UserAuthTestCase
from english.models import WordLearningStories, WordModel


class TestCollectData(UserAuthTestCase):
    """Testing data collection from a Word Study exercise."""

    @classmethod
    def setUpTestData(cls) -> None:
        """Set up test data.

        Add page path schema and word to dictionary.
        """
        super().setUpTestData()
        cls.path_schema = reverse_lazy('task:english_translate_demo')
        WordModel.objects.create(
            word_eng='word',
            user=cls.user,
        )

    def test_collect_number_word_displays(self) -> None:
        """Test collect the number of word displays."""
        task_conditions = {'timeout': 1, 'language_order': 'EN'}
        self.set_session(**{'task_conditions': task_conditions})
        self.get_auth_response(self.path_schema, method='post')

        self.assertEqual(
            WordLearningStories.objects.get(pk=1).display_count,
            1,
        )
