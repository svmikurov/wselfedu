"""Test home page module."""

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy


class HomePageTest(TestCase):
    """Home page view test."""

    def test_home_page_view(self) -> None:
        """Test Foreign home page 200 status."""
        response = self.client.get(reverse_lazy('foreign:main'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('WSE', str(response.content))
