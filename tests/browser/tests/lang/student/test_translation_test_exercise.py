"""Translation test the browser POM tests."""

from django.urls import reverse

from tests.browser.pages import TranslationTestPage
from tests.browser.tests import base, mixins
from tests.browser.tests.lang.fixture_mixins import SetUpAssignmentFixtureMixin


class TestTranslationTestPage(
    mixins.OpenPageMixin[TranslationTestPage],
    SetUpAssignmentFixtureMixin,
    base.BaseAuthTest,
):
    """Assigned translation test exercise page tests.

    Test via mixin that:
        - response status code is OK
        - page have correct title
    """

    def setUp(self) -> None:
        """Set up page."""
        super().setUp()
        self.page = TranslationTestPage(self._page)
        self.page.path = str(
            reverse(
                'lang:translation_english_test_mentorship',
                kwargs={'pk': self.assignment.pk},
            )
        )
