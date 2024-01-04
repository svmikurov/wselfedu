from typing import Generator

from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from english.models import WordModel
from users.models import UserModel


class TestUpdateWord(TestCase):
    def setUp(self):
        faker: Generator = Faker()
        fake_user_name: str = faker.user_name()
        fake_admin_name: str = faker.user_name()
        self.user = UserModel.objects.create_user(username=fake_user_name)
        self.admin = UserModel.objects.create_superuser(
            username=fake_admin_name,
        )

        self.word = WordModel.objects.create(
            words_eng='test',
            words_rus='тест',
            word_count='NC',
        )
        self.updated_word = {
            'words_eng': 'test',
            'words_rus': 'тест изменения слова',
            'word_count': 'ST',
        }

        self.update_word_url = reverse_lazy(
            'eng:words_update',
            kwargs={'pk': self.word.pk},
        )
        self.success_url = reverse_lazy('eng:words_list')
        self.redirect_nopermission_url = reverse_lazy('home')

    def test_get_update_by_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.update_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_update_by_admin(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.update_word_url, self.updated_word)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, 'Слово успешно изменено')
