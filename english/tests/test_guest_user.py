"""
Test views and available data for the not logged-in visitor.
"""

from django.test import Client, TestCase

HOME_PATH_NAME = 'home'
ENGLISH_HOME_PATH_NAME = 'english:home'
ACCOUNT_PATH_NAME = ...
WORDS_PATH_NAME = 'english:users_words'


class TestGuest(TestCase):
    """Test views and available data for the not logged-in visitor."""

    def setUp(self):
        self.client = Client()

    def test_guest_table_field_value(self):
        """Test the guest user table field value."""
        ...
