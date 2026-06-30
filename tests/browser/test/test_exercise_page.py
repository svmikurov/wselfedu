"""Testing exercise POM test."""

from playwright.sync_api import Locator, expect

from tests.factories.mock import (
    create_learnable_repo_mock,
    create_task_repo_mock,
)
from tests.factories.model import (
    create_testing_task,
    create_testing_task_dto,
    get_learnables,
)
from wse.di import django_site_container

from ..page.testing_exercise import TestingExercisePage
from .base import BaseTest


class BaseTestSetup(BaseTest):
    """Testing exercise page test configuration."""

    def setUp(self) -> None:
        super().setUp()
        self.page = TestingExercisePage(self._page)

        learnables = get_learnables()
        self.task = create_testing_task(learnables)
        task_dto = create_testing_task_dto(self.task)

        self.mock_learnable_repo = create_learnable_repo_mock(learnables)
        self.mock_task_repo = create_task_repo_mock(task_dto)

    @property
    def correct_answer_option_locator(self) -> Locator:
        """Correct option answer button locator."""
        return self.page.get_testing_option_locator(self.task.question_value)


class TestTestingExercisePage(BaseTestSetup):
    """Testing exercise POM test."""

    def test_page_have_testing_exercise_elements(self) -> None:
        # Act
        with django_site_container.use_cases.repositories.learnable.override(  # type: ignore
            self.mock_learnable_repo
        ):
            self.page.open()

            # Assert

            # - that page contain question text
            expect(self.page.question_text).to_be_visible()
            expect(self.page.question_text).to_contain_text('define')

            # - that page contain correct answer button
            expect(self.correct_answer_option_locator).to_be_visible()
