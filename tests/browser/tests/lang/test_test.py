"""Translation test the browser POM tests."""

from ...pages.lang.translation_test import TranslationTestPage
from .. import base, mixins


class TestTranslationTestPage(
    mixins.OpenPageMixin,
    base.BaseAuthTest,
):
    """Translation test page tests."""

    def setUp(self) -> None:
        """Set up page."""
        super().setUp()
        self.page = TranslationTestPage(self._page)
