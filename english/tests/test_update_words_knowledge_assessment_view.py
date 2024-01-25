from django.test import TestCase
from django.urls import reverse_lazy

from config.settings import MIN_KNOWLEDGE_ASSESSMENT, MAX_KNOWLEDGE_ASSESSMENT
from english.models import WordModel, WordUserKnowledgeRelation
from users.models import UserModel


class TestUpdateUserWordKnowledgeAssessment(TestCase):
    """Тест обновления в базе данных оценки пользователем знания слова.
       Обновлять может любой пользователь.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user = UserModel.objects.get(username='user1')
        self.word = WordModel.objects.get(pk=1)
        # Создаем отношение слово - пользователь в промежуточной модели.
        self.assessment = WordUserKnowledgeRelation.objects.create(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.user.pk),
        )
        # Задаем данные метода post.
        self.post_data = {'knowledge_assessment': '+1'}
        # Задаем url для изменения оценки.
        # Значение оценки по умолчанию равно "0".
        self.assessment_url = reverse_lazy(
            'eng:knowledge_assessment',
            kwargs={'word_id': self.word.pk},
        )
        # Задаем url переадресации после изменения оценки.
        self.success_url = reverse_lazy(
            'eng:repetition',
            kwargs={'task_status': 'question'},
        )

        # Задаем условия теста минимального и максимального уровня знания слова
        # на примере админа.
        self.min_knowledge_assessment = MIN_KNOWLEDGE_ASSESSMENT
        self.max_knowledge_assessment = MAX_KNOWLEDGE_ASSESSMENT
        self.min_word = WordModel.objects.get(pk=1)
        # self.max_word = WordModel.objects.get(pk=5)


    def test(self):
        # Аутентифицируем пользователя.
        self.client.force_login(self.user)
        # Тестируем передачу данных от button в views
        # Даем оценку "+1".
        response = self.client.post(self.assessment_url, self.post_data)
        # Получаем обновленное значение оценки.
        self.updated_assessment = WordUserKnowledgeRelation.objects.get(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.user.pk),
        )
        # Сравниваем статус.
        self.assertEqual(response.status_code, 302)
        # Сравниваем значение обновленной оценки.
        self.assertEqual(self.updated_assessment.knowledge_assessment, 1)

    def test_negative(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.assessment_url,
            {'knowledge_assessment': '+1'},
        )
        self.updated_assessment = WordUserKnowledgeRelation.objects.get(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.user.pk),
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.updated_assessment.knowledge_assessment, 0)

    # def test_min_knowledge_assessment(self):
    #     """Тест минимального значения уровня знания пользователем слова."""
    #     self.client.force_login(self.admin)


