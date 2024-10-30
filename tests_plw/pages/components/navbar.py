"""Representation of navbar for browser testing."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class NavbarComponent(POMPage):
    """Navbar representation."""

    def __init__(self, page: Page) -> None:
        """Construct the navbar representation."""
        super().__init__(page)
        self.page = page

        # Navbar container
        self.navbar = page.locator('.navbar-nav li')

        # Navigate links
        self.link_profile = (
            self.navbar.get_by_role('link', name='Личный кабинет')
        )  # fmt: skip
        self.link_foreign = (
            self.navbar.get_by_role('link', name='Иностранный язык')
        )  # fmt: skip
        self.link_glossary = (
            self.navbar.get_by_role('link', name='Глоссарий')
        )  # fmt: skip
        self.link_math = (
            self.navbar.get_by_role('link', name='Математика')
        )  # fmt: skip

        # Authentication links
        self.link_registration = (
            self.navbar.get_by_role('link', name='Регистрация')
        )  # fmt: skip
        self.link_login = self.navbar.get_by_role('link', name='Войти')
        self.link_logout = self.navbar.get_by_role('link', name='Выйти')

        # Navbar visible
        self.visible_anonymous = [
            self.link_foreign,
            self.link_glossary,
            self.link_math,
            self.link_registration,
            self.link_login,
        ]
        self.visible_logged = [
            self.link_profile,
            self.link_foreign,
            self.link_glossary,
            self.link_math,
            self.link_logout,
        ]

    def click_link_profile(self) -> None:
        """Click profile link."""
        self.link_profile.click()

    def click_link_foreign(self) -> None:
        """Click foreign words link."""
        self.link_foreign.click()

    def click_link_glossary(self) -> None:
        """Click glossary link."""
        self.link_glossary.click()

    def click_link_math(self) -> None:
        """Click math link."""
        self.link_math.click()

    def click_link_logout(self) -> None:
        """Click logout link."""
        self.link_logout.click()

    def click_link_login(self) -> None:
        """Click login link."""
        self.link_login.click()

    def click_link_registration(self) -> None:
        """Click registration link."""
        self.link_registration.click()
