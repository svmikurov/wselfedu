import logging
from typing import Generator

from django.contrib.auth.models import AnonymousUser
from django.template.response import TemplateResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse_lazy
from faker import Faker

from contrib_app.contrib_test import flash_message_test
from english.models import WordModel, CategoryModel
from english.views import WordListView
from users.models import UserModel

logger = logging.getLogger()

CREATE_URL = 'english:words_create'
"""Word creation URL.
"""
DETAIL_URL = 'english:words_detail'
"""Word details URL.
"""
UPDATE_URL = 'english:words_update'
"""Word update URL.
"""
DELETE_URL = 'english:words_delete'
"""Delete word URL.
"""
LIST_URL = 'english:word_list'
"""Word list URL.
"""
NOPERMISSION_URL = 'home'
"""Redirect URL if site visitor does not have permission to take action.
"""
NOPERMISSION_MSG = 'Вы пока не можете делать это'
"""Message for a site visitor about lack of permission to perform an action.
"""
DEFAULT_CATEGORY = 'Developer'
"""Automatically added category value if no category is selected.
"""


class TestCreateWord(TestCase):
    """Test create word."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        faker: Generator = Faker()
        fake_user_name: str = faker.user_name()
        self.fake_admin_name: str = faker.user_name()
        self.fake_user = UserModel.objects.create(username=fake_user_name,)
        self.fake_admin = UserModel.objects.create_superuser(
            username=self.fake_admin_name,
        )
        self.word_data = {'words_eng': 'test', 'words_rus': 'тест',
                          'word_count': 'NC'}
        CategoryModel.objects.create(name='Developer')
        self.url = reverse_lazy(CREATE_URL)
        self.nopermission_url = reverse_lazy(NOPERMISSION_URL)

    def test_get_auth_admin(self):
        """Test create word by admin, GET method page status 200."""
        self.client.force_login(self.fake_admin)
        response: TemplateResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_auth_admin(self):
        """Test create word by admin, POST method page status 200."""
        self.client.force_login(self.fake_admin)
        response = self.client.post(self.url, self.word_data)
        self.assertRedirects(response, self.url, 302)
        flash_message_test(response, 'Слово успешно добавлено')

    def test_add_category_default_by_admin(self):
        """Test add default category and user_name to form."""
        self.client.force_login(self.fake_admin)
        self.client.post(self.url, self.word_data)
        added_word = WordModel.objects.get(
            words_eng=self.word_data['words_eng']
        )
        assert added_word.category.name == DEFAULT_CATEGORY
        assert added_word.user.username == self.fake_admin_name

    def test_get_create_word_by_user(self):
        """Test create word by logged-in user, GET method page status 302."""
        self.client.force_login(self.fake_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_post_create_word_by_user(self):
        """Test create word by logged-in user, POST method page status 302."""
        self.client.force_login(self.fake_user)
        response = self.client.post(self.url, self.word_data)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_get_create_word_by_anonymous(self):
        """Test create word by not logged-in user, GET method page status 302.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_post_create_word_by_anonymous(self):
        """Test create word by not logged-in user, POST method page status 302.
        """
        response = self.client.post(self.url, self.word_data)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)


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
            words_eng='test', words_rus='тест', word_count='NC',
        )
        self.updated_word = {
            'words_eng': 'test', 'words_rus': 'тест изменения слова',
            'word_count': 'ST',
        }
        self.url = reverse_lazy(UPDATE_URL)
        self.word_url = reverse_lazy(UPDATE_URL, kwargs={'pk': self.word.pk})
        self.success_url = reverse_lazy(LIST_URL)
        self.nopermission_url = reverse_lazy(NOPERMISSION_URL)

    def test_get_update_by_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_update_by_admin(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.word_url, self.updated_word)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, 'Слово успешно изменено')

    def test_get_update_word_by_user(self):
        """Test update word by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.word_url)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_post_update_word_by_user(self):
        """Test update word by logged-in user, POST method page status 200."""
        self.client.force_login(self.user)
        response = self.client.post(self.word_url, self.updated_word)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_get_update_word_by_anonymous(self):
        """Test update word by not logged-in user, GET method page status 200.
        """
        response = self.client.get(self.word_url)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)

    def test_post_update_word_by_anonymous(self):
        """Test update word by logged-in user, POST method page status 200."""
        response = self.client.post(self.word_url, self.updated_word)
        self.assertRedirects(response, self.nopermission_url, 302)
        flash_message_test(response, NOPERMISSION_MSG)


class TestDeleteWord(TestCase):
    """Test delete word."""

    def setUp(self):
        faker: Generator = Faker()
        admin_name = faker.user_name()
        self.admin_user = UserModel.objects.create_superuser(
            username=admin_name,
        )
        self.another_word = WordModel.objects.create(
            words_eng='another', words_rus='другое', word_count='OW',
        )
        self.deleted_word = WordModel.objects.create(
            words_eng='test', words_rus='тест', word_count='OW',
        )
        self.url = reverse_lazy(DELETE_URL)
        self.word_url = reverse_lazy(
            'english:words_delete', kwargs={'pk': self.deleted_word.pk},
        )
        self.success_url = reverse_lazy(LIST_URL)

    def test_get_delete_word_by_admin_user(self):
        """Test delete word by admin, GET method page status."""
        self.client.force_login(self.admin_user)
        response = self.client.get(self.word_url)
        self.assertEqual(response.status_code, 200)

    def test_post_delete_word_by_admin_user(self):
        """Test delete word by admin, POST method page status."""
        self.client.force_login(self.admin_user)
        response = self.client.post(self.word_url)
        self.assertRedirects(response, self.success_url, 302)

    def test_get_delete_word_by_user(self):
        ...

    def test_post_delete_word_by_user(self):
        ...

    def test_get_delete_word_by_anonymous(self):
        ...

    def test_post_delete_word_by_anonymous(self):
        ...


class TestWordListView(TestCase):
    """Test word list view."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse_lazy(LIST_URL)

    def test_status_words_list_page(self):
        """Тест статус 200 страницы списка слов."""
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = WordListView.as_view()(request)
        self.assertTrue(response.status_code, 200)

    def test_search_word(self):
        """Тест фильтра списка по слову."""
        # filter by english word
        search_param = {'search_word': 'word02'}
        response = self.client.get(self.url, search_param)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, 'word02')
        self.assertNotContains(response, 'word01')

        # filter by russian word
        search_param = {'search_word': 'слово01'}
        response = self.client.get(self.url, search_param)
        self.assertTrue(response.status_code, 200)
        self.assertContains(response, 'слово01')
        self.assertNotContains(response, 'слово02')


class TestDetailWord(TestCase):
    pass
