"""Test the about page."""

from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestAbout(TestCase):
    """Test the page about project.

    The page is accessible to unauthorized users.
    """

    def setUp(self) -> None:
        """Set up the test data."""
        self.client = Client()
        self.url = reverse_lazy('about')

    def test_page_status(self) -> None:
        """Test the page status."""
        response = self.client.get(self.url)
        assert response.status_code == HTTPStatus.OK
