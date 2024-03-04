"""
Registered user data confidentiality test module.
Does not test application presentation to not logged-in user.
"""
from unittest import skip

from django.test import Client, TestCase
from django.urls import reverse_lazy

from english.models import WordModel
from users.models import UserModel

WORD_LIST_PATH = 'english:users_words'
"""User word list path name.
"""


class TestUserWordListPageStatusAndAccess(TestCase):
    """Test user word list page status and access to list for any users."""

    fixtures = ['english/tests/fixtures/wse-fixtures-2.json']
    TestCase.maxDiff = None

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
            WORD_LIST_PATH, kwargs={'pk': self.user_owner.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_status_by_not_owner_account(self):
        """Test users words list view by not owner account, page status 403."""
        self.client.force_login(self.user_not_owner)
        response = self.client.get(reverse_lazy(
            WORD_LIST_PATH, kwargs={'pk': self.user_owner.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_page_status_by_visitor(self):
        """Test users words list view by not logged-in user, page status 302.
        """
        response = self.client.get(reverse_lazy(
            WORD_LIST_PATH, kwargs={'pk': self.user_owner.pk})
        )
        self.assertEqual(response.status_code, 302)


class TestShowOnlyUserData(TestCase):
    """Test the user word list confidentiality."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.client = Client()
        self.user_id = 2
        self.user = UserModel.objects.get(pk=self.user_id)
        self.url = reverse_lazy(WORD_LIST_PATH, kwargs={'pk': self.user_id})

    def test_show_only_user_word_list(self):
        """Test show only user word list on page."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        current_queryset = response.context.get('words')
        expected_queryset = WordModel.objects.filter(user_id=self.user_id)

        self.assertQuerySetEqual(current_queryset, expected_queryset)

    @skip
    def test_user_word_list_content(self):
        """Test contents of the user's word list."""
