"""Testing exercise POM test."""

from playwright.sync_api import expect

from tests.browser.pom.page.testing_exercise import TestingExercisePage

from .pom.test.base import BaseTest


class TestTestingExercisePage(BaseTest):
    """Testing exercise POM test."""

    def setUp(self) -> None:
        super().setUp()
        self.page = TestingExercisePage(self._page)

    def test_page_have_question_text(self) -> None:
        self.page.open()

        expect(self.page.question_text).to_be_visible()
        expect(self.page.question_text).to_have_text('Question text')
