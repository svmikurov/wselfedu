"""
This module tests data collection for analytical purposes.
Data is collected from the “Learning words” exercise.
"""

from django.test import TestCase

from django.urls import reverse_lazy

from contrib.mixins_tests import TestMixin
from english.models import WordLearningStories, WordModel
from users.models import UserModel


class TestCollectData(TestMixin, TestCase):
    """Testing data collection from a Word Study exercise."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserModel.objects.create_user(
            username='user',
            password='password',
        )
        cls.url = reverse_lazy('task:english_translate_demo')
        WordModel.objects.create(word_eng='word', user=cls.user)

    def test_collect_number_word_displays(self):
        """Test collect the number of word displays."""
        task_conditions = {'timeout': 1, 'language_order': 'EN'}
        self.set_session(**{'task_conditions': task_conditions})
        self.client.force_login(self.user)
        self.client.post(self.url)

        self.assertEqual(
            WordLearningStories.objects.get(pk=1).display_count,
            1,
        )
