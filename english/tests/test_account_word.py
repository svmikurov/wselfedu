from django.test import Client, TestCase
from django.urls import reverse_lazy

from users.models import UserModel

WORDS_URL_NAME = 'english:users_words'


class TestAccountWordView(TestCase):
    """Тест таблицы слов зарегистрированного пользователя."""

    fixtures = ['english/tests/fixtures/wse-fixtures-2.json']

    def setUp(self):
        self.client = Client()
        account_owner_pk = 2
        not_owner_pk = 3
        self.user_owner = UserModel.objects.get(pk=account_owner_pk)
        self.user_not_owner = UserModel.objects.get(pk=not_owner_pk)

    def test_page_status_by_owner_account(self):
        """Test users words list view by owner account, page status 200."""
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse_lazy(
            WORDS_URL_NAME, kwargs={'pk': self.user_owner.pk}))
        self.assertEqual(response.status_code, 200)

    def test_page_status_by_not_owner_account(self):
        """Test users words list view by not owner account, page status 403."""
        self.client.force_login(self.user_not_owner)
        response = self.client.get(reverse_lazy(
            WORDS_URL_NAME, kwargs={'pk': self.user_owner.pk}))
        self.assertEqual(response.status_code, 403)

    def test_page_status_by_visitor(self):
        """Test users words list view by not logged-in user, page status 302.
        """
        # Доработать тест и представление, сейчас тестируется только защита от
        # неправомерного доступа.
        response = self.client.get(reverse_lazy(
            WORDS_URL_NAME, kwargs={'pk': self.user_owner.pk}))
        self.assertEqual(response.status_code, 302)
