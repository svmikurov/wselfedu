"""Test word study progres."""

from unittest import skip

from django.test import TestCase
from django.urls import reverse_lazy

from config.consts import WORD_PROGRES_MAX, WORD_PROGRES_MIN
from english.models import WordModel, WordUserKnowledgeRelation
from english.orm_queries import (
    get_knowledge_assessment,
)
from users.models import UserModel


class TestUpdateProgres(TestCase):
    """Test update Word study progres."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures.json']

    def setUp(self) -> None:
        """Set up test data."""
        self.user = UserModel.objects.get(pk=2)
        self.word_min_assessment = WordModel.objects.get(pk=6)  # 0
        self.word_max_assessment = WordModel.objects.get(pk=5)  # 11
        self.word_middle_assessment = WordModel.objects.get(pk=3)  # 7
        self.expected_updated_assessment = 6
        self.new_word_data = {
            'user': UserModel.objects.get(pk=1),
            'word_eng': 'test',
            'word_rus': 'тест',
        }

        self.assessment_up = {'action': '+1'}
        self.assessment_down = {'action': '-1'}

        assessment_url = 'english:knowledge_assessment'
        self.min_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_min_assessment.pk}
        )
        self.middle_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_middle_assessment.pk}
        )
        self.max_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_max_assessment.pk}
        )
        self.redirect_url = reverse_lazy('english:word_study_question')

    def test_add_knowledge_assessment(self) -> None:
        """Test get or create knowledge_assessment."""
        new_word_pk = WordModel.objects.create(**self.new_word_data).pk
        self.assertFalse(
            WordUserKnowledgeRelation.objects.filter(
                word_id=new_word_pk
            ).exists()
        )
        get_knowledge_assessment(new_word_pk, self.user.pk)
        self.assertTrue(
            WordUserKnowledgeRelation.objects.filter(
                word_id=new_word_pk
            ).exists()
        )

    @skip
    def test_know_before_max(self) -> None:
        """Test mark as know Word before max value."""
        word_id = ...
        url = reverse_lazy('english:word_choice')
        payload = {'action': 'know', 'id': word_id}

        self.client.force_login(self.user)
        self.client.post(url, payload)

    @skip
    def test_min_knowledge_assessment(self) -> None:
        """Test to reduce the minimum level of user assessment."""
        self.client.force_login(self.user)
        self.client.post(self.min_assessment_url, self.assessment_down)
        given_assessment = get_knowledge_assessment(
            self.word_min_assessment.pk,
            self.user.pk,
        )
        self.assertEqual(given_assessment, WORD_PROGRES_MIN)

    @skip
    def test_max_knowledge_assessment(self) -> None:
        """Test to increase the maximum level of user assessment."""
        self.client.force_login(self.user)
        self.client.post(self.max_assessment_url, self.assessment_up)
        given_assessment = get_knowledge_assessment(
            self.word_max_assessment.pk,
            self.user.pk,
        )
        self.assertEqual(given_assessment, WORD_PROGRES_MAX)
