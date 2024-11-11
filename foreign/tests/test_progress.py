"""Test word study progres."""

from unittest import skip

from django.test import TestCase
from django.urls import reverse_lazy

from config.constants import (
    PROGRESS_MAX,
    PROGRESS_MIN,
)
from foreign.models import (
    Word,
    WordProgress,
)
from foreign.queries import (
    get_progress,
)
from users.models import UserApp


class TestUpdateProgres(TestCase):
    """Test update Word study progres."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.user = UserApp.objects.get(pk=2)
        self.word_min_assessment = Word.objects.get(pk=6)  # 0
        self.word_max_assessment = Word.objects.get(pk=5)  # 11
        self.word_middle_assessment = Word.objects.get(pk=3)  # 7
        self.expected_updated_assessment = 6
        self.new_word_data = {
            'user': UserApp.objects.get(pk=1),
            'foreign_word': 'test',
            'native_word': 'тест',
        }

        self.assessment_up = {'action': '+1'}
        self.assessment_down = {'action': '-1'}

        assessment_url = 'foreign:progress'
        self.min_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_min_assessment.pk}
        )
        self.middle_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_middle_assessment.pk}
        )
        self.max_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_max_assessment.pk}
        )
        self.redirect_url = reverse_lazy('foreign:word_study_question')

    def test_add_progress(self) -> None:
        """Test get or create progress."""
        new_word_pk = Word.objects.create(**self.new_word_data).pk
        self.assertFalse(
            WordProgress.objects.filter(word_id=new_word_pk).exists()
        )
        get_progress(new_word_pk, self.user.pk)
        self.assertTrue(
            WordProgress.objects.filter(word_id=new_word_pk).exists()
        )

    @skip
    def test_know_before_max(self) -> None:
        """Test mark as know Word before max value."""
        word_id = 3
        url = reverse_lazy('foreign:progress')
        payload = {'action': 'know', 'id': word_id}

        progress_before = WordProgress.objects.get(word_id=word_id)
        self.client.force_login(self.user)
        self.client.post(url, payload)
        progress_after = WordProgress.objects.get(word_id=word_id)
        assert bool(progress_after == progress_before + 1)

    def test_min_progress(self) -> None:
        """Test to reduce the minimum level of user assessment."""
        self.client.force_login(self.user)
        self.client.post(self.min_assessment_url, self.assessment_down)
        given_assessment = get_progress(
            self.word_min_assessment.pk,
            self.user.pk,
        )
        self.assertEqual(given_assessment, PROGRESS_MIN)

    @skip
    def test_max_progress(self) -> None:
        """Test to increase the maximum level of user assessment."""
        self.client.force_login(self.user)
        self.client.post(self.max_assessment_url, self.assessment_up)
        given_assessment = get_progress(
            self.word_max_assessment.pk,
            self.user.pk,
        )
        self.assertEqual(given_assessment, PROGRESS_MAX)
