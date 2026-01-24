"""Assignment list page."""

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from tests.browser.pages import base
from tests.browser.tests.lang import fixture_mixins


class AssignmentsPage(
    fixture_mixins.SetUpAssignmentFixtureMixin, base.BasePage
):
    """Assignment list page."""

    title = _('lang.english.tasks.page.index.title')
    path = str(reverse_lazy('lang:english_tasks'))

    def goto_exercise(self, exercise_name: str) -> None:
        """Go to assigned exercise."""
        locator = self._page.get_by_text(exercise_name)
        locator.click()
