"""Exercise POM test."""

from http import HTTPStatus

from .pom.page.base import BasePage
from .pom.test.base import BaseTest


class ExercisePage(BasePage):
    """Exercise POM page."""

    path = '/exercise/'


class TestExercisePage(BaseTest):
    """Exercise POM test."""

    def setUp(self) -> None:
        """Set up page."""
        super().setUp()
        self.page = ExercisePage(self._page)

    def test_response_status_ok(self) -> None:
        # Act
        response = self.page.open()

        # Assert
        assert response
        assert response.status == HTTPStatus.OK
