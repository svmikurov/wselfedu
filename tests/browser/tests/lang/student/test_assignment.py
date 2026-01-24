"""Assigned exercise list page browser POM tests."""

from playwright.sync_api import expect

from tests.browser.pages import AssignmentsPage, TranslationTestPage
from tests.browser.tests import base, mixins
from tests.browser.tests.lang import fixture_mixins


class TestAssignmentsPage(
    mixins.OpenPageMixin[AssignmentsPage],
    fixture_mixins.SetUpAssignmentFixtureMixin,
    base.BaseAuthTest,
):
    """Test the Assignments for student page.

    Test via mixin that:
        - response status code is OK
        - page have correct title
    """

    def setUp(self) -> None:
        """Set up page."""
        super().setUp()
        self.page = AssignmentsPage(self._page)
        self.page.open()

    def test_goto_assigned_exercise(self) -> None:
        """Test go to assigned exercise the user action."""
        # Act
        self.page.goto_exercise(exercise_name=self.assignment.exercise.name)
        # Assert
        expect(self._page).to_have_title(TranslationTestPage.title)
