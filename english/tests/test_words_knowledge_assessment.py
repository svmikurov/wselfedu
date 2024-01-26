from django.test import TestCase
from django.urls import reverse_lazy

from config.settings import MIN_KNOWLEDGE_ASSESSMENT, MAX_KNOWLEDGE_ASSESSMENT
from english.models import WordModel, WordUserKnowledgeRelation
from english.services.words_knowledge_assessment import (
    get_word_knowledge_assessment,
    get_or_create_knowledge_assessment,
)
from users.models import UserModel


class TestWordsKnowledgeAssessment(TestCase):
    """Тест обновления в базе данных оценки пользователем знания слова.

    Минимальное значение оценки "MIN_KNOWLEDGE_ASSESSMENT" = "0",
    максимальное "MAX_KNOWLEDGE_ASSESSMENT" = "11".
    Шаг увеличения = "+1", уменьшения = "-1".
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user = UserModel.objects.get(pk=2)
        self.word_min_assessment = WordModel.objects.get(pk=1)     # 0
        self.word_max_assessment = WordModel.objects.get(pk=5)     # 11
        self.word_middle_assessment = WordModel.objects.get(pk=3)  # 7
        self.expected_updated_assessment = 6
        self.new_word_data = {'words_eng': 'test', 'words_rus': 'тест'}

        self.assessment_up = {'knowledge_assessment': '+1'}
        self.assessment_down = {'knowledge_assessment': '-1'}

        assessment_url = 'eng:knowledge_assessment'
        self.min_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_min_assessment.pk}
        )
        self.middle_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_middle_assessment.pk}
        )
        self.max_assessment_url = reverse_lazy(
            assessment_url, kwargs={'word_id': self.word_max_assessment.pk}
        )
        self.redirect_url = reverse_lazy(
            'eng:repetition', kwargs={'task_status': 'question'}
        )

    def test_add_knowledge_assessment(self):
        """Тест get_or_create_knowledge_assessment.
        """
        new_word_pk = WordModel.objects.create(**self.new_word_data).pk
        self.assertFalse(WordUserKnowledgeRelation.objects.filter(
            word_id=new_word_pk
        ).exists())
        get_or_create_knowledge_assessment(new_word_pk, self.user.pk)
        self.assertTrue(WordUserKnowledgeRelation.objects.filter(
            word_id=new_word_pk
        ).exists())

    def test_update_knowledge_assessment(self):
        """Тест изменения пользователем оценки знания слова.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            self.middle_assessment_url, self.assessment_down
        )
        updated_assessment = get_word_knowledge_assessment(
            self.user.pk, self.word_middle_assessment.pk,
        )
        self.assertEqual(updated_assessment, self.expected_updated_assessment)
        self.assertRedirects(response, self.redirect_url, 302)

    def test_min_knowledge_assessment(self):
        """Тест минимального уровня оценки пользователем знания слова.
        """
        self.client.force_login(self.user)
        self.client.post(self.min_assessment_url, self.assessment_down)
        given_assessment = get_word_knowledge_assessment(
            self.user.pk, self.word_min_assessment.pk
        )
        self.assertEqual(given_assessment, MIN_KNOWLEDGE_ASSESSMENT)

    def test_max_knowledge_assessment(self):
        """Тест максимального уровня оценки пользователем знания слова.
        """
        self.client.force_login(self.user)
        self.client.post(self.max_assessment_url, self.assessment_up)
        given_assessment = get_word_knowledge_assessment(
            self.user.pk, self.word_max_assessment.pk
        )
        self.assertEqual(given_assessment, MAX_KNOWLEDGE_ASSESSMENT)