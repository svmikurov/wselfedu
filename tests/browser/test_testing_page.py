"""Testing exercise POM test."""

from playwright.sync_api import expect

from tests.browser.pom.page.testing_exercise import TestingExercisePage
from tests.factories.mock import (
    create_learnable_repo_mock,
    create_mock_task_repo,
)
from tests.factories.model import (
    create_testing_task,
    create_testing_task_dto,
    get_learnables,
)
from wse.di.application import ApplicationContainer

from .pom.test.base import BaseTest


class TestTestingExercisePage(BaseTest):
    """Testing exercise POM test."""

    def setUp(self) -> None:
        super().setUp()
        self.page = TestingExercisePage(self._page)

    def test_page_have_question_text(self) -> None:
        # Arrange
        container = ApplicationContainer()

        learnables = get_learnables()
        task = create_testing_task(learnables)
        task_do = create_testing_task_dto(task)

        mock_learnable_repo = create_learnable_repo_mock(learnables)
        mock_task_repo = create_mock_task_repo(task_do)

        # Act
        with (
            container.repositories.learnable.override(mock_learnable_repo),
            container.repositories.task.override(mock_task_repo),
        ):
            self.page.open()

            expect(self.page.question_text).to_be_visible()
            expect(self.page.question_text).to_have_text('Question text')
