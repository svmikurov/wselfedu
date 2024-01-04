from typing import Generator

from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from english.models import WordModel
from users.models import UserModel


class TestDeleteWord(TestCase):
    def setUp(self):
        faker: Generator = Faker()
        admin_name = faker.user_name()
        self.admin_user = UserModel.objects.create_superuser(
            username=admin_name,
        )

        self.another_word = WordModel.objects.create(
            words_eng='another',
            words_rus='другое',
            word_count='OW',
        )
        self.deleted_word = WordModel.objects.create(
            words_eng='test',
            words_rus='тест',
            word_count='OW',
        )

        self.delete_word_url = reverse_lazy(
            'eng:words_delete',
            kwargs={'pk': self.deleted_word.pk},
        )
        self.success_url = reverse_lazy('eng:words_list')

    def test_get_delete_word_by_admin_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.delete_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_word_by_admin_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.delete_word_url)
        self.assertRedirects(response, self.success_url, 302)
