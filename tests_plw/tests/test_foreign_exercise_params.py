"""Test the foreign words exercise conditions choice page."""

from http import HTTPStatus
from urllib.parse import urlparse

from playwright.sync_api import expect

from config.constants import NOT_CHOICES, TO_NATIVE, TODAY
from tests_plw.pages import ForeignExerciseParamsPage
from tests_plw.tests.base import POMTest


class TestForeignWordsExerciseConditionsChoicePage(POMTest):
    """Test the foreign words exercise conditions choice page."""

    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.test_page = ForeignExerciseParamsPage(self.page)
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

        # Favorites word checkbox.
        expect(page.favorites_choice).not_to_be_checked()
        # Translate order choice.
        expect(page.order_choice).to_have_value(TO_NATIVE)
        # Word category choice.
        expect(page.category_choice).to_have_value('0')
        # Word source choice.
        expect(page.source_choice).to_have_value('0')
        # Word adding edge period choice.
        expect(page.start_period_choice).to_have_value(NOT_CHOICES)
        expect(page.end_period_choice).to_have_value(TODAY)
        # Study progress checkboxes.
        expect(page.study_progress_label).to_be_visible()
        expect(page.repeat_progress_label).to_be_visible()
        expect(page.repeat_progress_label).to_be_visible()
        expect(page.examination_progress_label).to_be_visible()
        expect(page.study_progress_choice).to_be_checked()
        expect(page.repeat_progress_choice).not_to_be_checked()
        expect(page.examination_progress_choice).not_to_be_checked()
        expect(page.know_progress_choice).not_to_be_checked()
        # Answer timeout choice.
        expect(page.timeout_choice).to_have_value('5')
