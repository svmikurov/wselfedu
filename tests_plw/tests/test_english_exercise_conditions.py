"""Test English exercise conditions choice page."""

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
        self.user = self.create_user()
        self.authorize_test_page(user=self.user)

    def test_status(self) -> None:
        """Test http status."""
        self.response = self.test_page.navigate(page_url=self.page_url)
        assert self.response.status == 200
