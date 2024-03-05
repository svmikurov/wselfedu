from unittest import skip

from django.test import Client, TestCase

from english.services import get_words_for_study


class TestGetWordFordStudy(TestCase):
    """Test get word for study."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.client = Client()
        self.user_id = 3

    @skip
    def test_get_words_for_study(self):
        """Test get words for study."""
        get_words_for_study(self.lookup_params, self.user_id)
        ...
