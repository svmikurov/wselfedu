from django.test import TestCase
from django.urls import reverse_lazy

from english.models import WordModel, WordUserKnowledgeRelation
from users.models import UserModel


class TestUpdateKnowledgeAssessment(TestCase):

    def setUp(self):
        # Создаем пользователя.
        admin_name: str = 'admin_user'
        self.admin_user = UserModel.objects.create_superuser(
            username=admin_name,
        )
        # Добавляем слово в БД.
        self.word = WordModel.objects.create(
            user_id=self.admin_user.pk,
            words_eng='test',
            words_rus='тест',
            word_count='NC',
        )
        # Создаем отношение слово - пользователь в промежуточной модели.
        self.assessment = WordUserKnowledgeRelation.objects.create(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.admin_user.pk),
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

    def test(self):
        # Аутентифицируем пользователя.
        self.client.force_login(self.admin_user)
        # Тестируем передачу данных от button в views
        # Даем оценку "+1".
        response = self.client.post(self.assessment_url, self.post_data)
        # Получаем обновленное значение оценки.
        self.updated_assessment = WordUserKnowledgeRelation.objects.get(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.admin_user.pk),
        )
        # Сравниваем статус.
        self.assertEqual(response.status_code, 302)
        # Сравниваем значение обновленной оценки.
        self.assertEqual(self.updated_assessment.knowledge_assessment, 1)

    def test_negative(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(
            self.assessment_url,
            {'knowledge_assessment': '+1'},
        )
        self.updated_assessment = WordUserKnowledgeRelation.objects.get(
            word=WordModel.objects.get(pk=self.word.pk),
            user=UserModel.objects.get(pk=self.admin_user.pk),
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.updated_assessment.knowledge_assessment, 0)
