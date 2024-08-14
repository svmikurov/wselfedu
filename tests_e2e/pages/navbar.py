"""The site pages navbar representation class."""

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class NavbarPageComponent(POMPage):
    """The site page navbar representation class."""

    def __init__(self, page: Page) -> None:
        """Construct navbar representation."""
        super().__init__(page)
        self.tutorial_link = self.page.get_by_text('Справочник пользователя')
        self.toggle_btn = self.page.get_by_label('Toggle navigation')

    def expand_menu(self) -> None:
        """Expand the menu."""
        if self.toggle_btn.is_visible():
            self.toggle_btn.click()
