"""Testing exercise POM test."""

from playwright.sync_api import expect

from tests.browser.pom.page.testing_exercise import TestingExercisePage
from tests.factories.mock import (
    create_learnable_repo_mock,
)
from tests.factories.model import (
    get_learnables,
)
from wse.di.application import ApplicationContainer

from .pom.test.base import BaseTest


class TestTestingExercisePage(BaseTest):
    """Testing exercise POM test."""

    def setUp(self) -> None:
        super().setUp()
        self.page = TestingExercisePage(self._page)
        self.container = ApplicationContainer()
        self.repositories = self.container.repositories
        self.mock_learnable_repo = create_learnable_repo_mock(get_learnables())

    def test_page_have_question_text(self) -> None:
        # Act
        with self.repositories.learnable.override(self.mock_learnable_repo):
            self.page.open()

            # Assert
            expect(self.page.question_text).to_be_visible()
            expect(self.page.question_text).to_have_text('define')
