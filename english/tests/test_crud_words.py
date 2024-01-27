import logging
from typing import Generator

from django.template.response import TemplateResponse
from django.test import TestCase
from django.urls import reverse_lazy
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from english.models import WordModel
from users.models import UserModel

logger = logging.getLogger()


class TestAddWord(TestCase):

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.add_word_url = reverse_lazy('english:words_create')
        self.redirect_nopermission_url = reverse_lazy('home')

        faker: Generator = Faker()
        fake_user_name: str = faker.user_name()
        self.fake_admin_name: str = faker.user_name()
        self.fake_user = UserModel.objects.create(username=fake_user_name,)
        self.fake_admin = UserModel.objects.create_superuser(
            username=self.fake_admin_name,
        )

        self.added_word_data = {
            'words_eng': 'test',
            'words_rus': 'тест',
            'word_count': 'NC',
        }
        self.default_word_category_name = "category3"

    def test_get_auth_admin(self):
        self.client.force_login(self.fake_admin)
        response: TemplateResponse = self.client.get(self.add_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_auth_admin(self):
        self.client.force_login(self.fake_admin)
        response = self.client.post(self.add_word_url, self.added_word_data)
        self.assertRedirects(response, self.add_word_url, 302)
        flash_message_test(response, 'Слово успешно добавлено')

    def test_add_category_default_by_admin(self):
        """Test added default category and user_name to form."""
        self.client.force_login(self.fake_admin)
        self.client.post(self.add_word_url, self.added_word_data)
        added_word = WordModel.objects.get(
            words_eng=self.added_word_data['words_eng']
        )
        assert added_word.category.name == self.default_word_category_name
        assert added_word.user.username == self.fake_admin_name
        assert added_word.user.username != self.fake_user

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
            'english:words_update',
            kwargs={'pk': self.word.pk},
        )
        self.success_url = reverse_lazy('english:words_list')
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
            'english:words_delete',
            kwargs={'pk': self.deleted_word.pk},
        )
        self.success_url = reverse_lazy('english:words_list')

    def test_get_delete_word_by_admin_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(self.delete_word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_word_by_admin_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(self.delete_word_url)
        self.assertRedirects(response, self.success_url, 302)
