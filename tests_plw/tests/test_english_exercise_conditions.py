"""Test English exercise conditions choice page."""
import logging
import re
from http import HTTPStatus
from unittest import skip
from urllib.parse import urlparse

from playwright.sync_api import expect

import config.constants as const
from tests_plw.pages.english_exercise_conditions import (
    EnglishExerciseConditionsChoicePage,
)
from tests_plw.tests.base import POMTest


class TestEnglishExerciseConditionsChoicePage(POMTest):
    """Test English exercise conditions choice page."""

    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.test_page = EnglishExerciseConditionsChoicePage(self.page)
        self.page_path = self.test_page.path
        self.authorize_test_page()
        self.response = self.test_page.navigate(page_url=self.page_url)

    def test_http_status(self) -> None:
        """Test http status."""
        response_path = urlparse(self.response.url).path
        assert response_path == self.page_path
        assert self.response.status == HTTPStatus.OK

    def test_default_exercise_conditions(self) -> None:
        """Test default exercise conditions."""
        page = self.test_page
        expect(page.favorites_choice).not_to_be_checked()
        expect(page.language_order_choice).to_have_value('RN')
