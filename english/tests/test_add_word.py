from typing import Generator

from django.test import TestCase
from django.urls import reverse_lazy
from django.utils import timezone
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel


class TestAddWord(TestCase):

    def setUp(self):
        self.add_word_url = reverse_lazy('eng:words_create')
        self.redirect_nopermission_url = reverse_lazy('home')

        faker: Generator = Faker()
        fake_username: str = faker.user_name()
        self.fake_user = UserModel.objects.create(
            username=fake_username,
        )
        fake_username_admin: str = faker.user_name()
        self.fake_admin_user = UserModel.objects.create(
            username=fake_username_admin,
            is_superuser=True,
        )
        self.fake_name_not_owner = faker.user_name()
        self.fake_user_not_owner = UserModel.objects.create(
            username=self.fake_name_not_owner
        )

        self.word_data = {
            'words_eng': 'test',
            'words_rus': 'тест',
            'created_at': timezone.now,
            # 'updated_at': timezone.now,
        }

    def test_get_auth_admin(self):
        self.client.force_login(self.fake_admin_user)
        response = self.client.get(self.add_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_auth_admin(self):
        self.client.force_login(self.fake_admin_user)
        response = self.client.post(self.add_word_url, self.word_data)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
        flash_message_test(response, 'Слово успешно добавлено')

    def test_get_auth_user(self):
        self.client.force_login(self.fake_user)
        response = self.client.get(self.add_word_url)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)

    def test_post_auth_user(self):
        self.client.force_login(self.fake_user)
        response = self.client.post(self.add_word_url, self.word_data)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
