import logging
from typing import Generator

from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from users.models import UserModel

logger = logging.getLogger()


class TestAddWord(TestCase):

    def setUp(self):
        self.add_word_url = reverse_lazy('eng:words_create')
        self.redirect_nopermission_url = reverse_lazy('home')

        faker: Generator = Faker()
        fake_user_name: str = faker.user_name()
        fake_admin_name: str = faker.user_name()
        self.fake_user = UserModel.objects.create(username=fake_user_name,)
        self.fake_admin = UserModel.objects.create_superuser(
            username=fake_admin_name,
        )

        self.added_word_data = {
            'words_eng': 'test',
            'words_rus': 'тест',
            'word_count': 'NC',
        }

    def test_get_auth_admin(self):
        self.client.force_login(self.fake_admin)
        response: TemplateResponse = self.client.get(self.add_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_auth_admin(self):
        self.client.force_login(self.fake_admin)
        logger.debug('test_post_auth_admin')
        response = self.client.post(self.add_word_url, self.added_word_data)
        self.assertRedirects(response, self.add_word_url, 302)
        flash_message_test(response, 'Слово успешно добавлено')

    def test_get_auth_user(self):
        self.client.force_login(self.fake_user)
        response = self.client.get(self.add_word_url)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
        flash_message_test(response, 'Вы пока не можете делать это')

    def test_post_auth_user(self):
        self.client.force_login(self.fake_user)
        response = self.client.post(self.add_word_url, self.added_word_data)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
        flash_message_test(response, 'Вы пока не можете делать это')

    def test_not_auth_user(self):
        response = self.client.get(self.add_word_url)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
        flash_message_test(response, 'Вы пока не можете делать это')

    def test_post_not_auth_user(self):
        response = self.client.post(self.add_word_url, self.added_word_data)
        self.assertRedirects(response, self.redirect_nopermission_url, 302)
        flash_message_test(response, 'Вы пока не можете делать это')
