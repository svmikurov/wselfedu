"""Test navbar."""

import pytest
from playwright.sync_api import expect

from tests_plw.page_components.navbar import NavbarComponent
from tests_plw.pages import (
    ForeignPage,
    GlossaryPage,
    HomePage,
    LoginPage,
    MathExerciseParamsPage,
    ProfilePage,
    RegistrationPage,
)
from tests_plw.tests.base import POMTest


class TestNavbarMixin:
    """Test navbar, the mixin."""

    __test__ = False
    test_page: NavbarComponent

    def test_link_foreign(self) -> None:
        """Test the foreign links."""
        self.test_page.click_link_foreign()
        self.test_page.test_title(ForeignPage.title)

    def test_link_glossary(self) -> None:
        """Test the glossary link."""
        self.test_page.click_link_glossary()
        self.test_page.test_title(GlossaryPage.title)

    def test_link_mathematics(self) -> None:
        """Test the mathematics link."""
        self.test_page.click_link_math()
        self.test_page.test_title(MathExerciseParamsPage.title)


class TestNavbarLogged(TestNavbarMixin, POMTest):
    """Test navbar for logged user."""

    __test__ = True

    def setUp(self) -> None:
        """Set up page data."""
        self.test_page = NavbarComponent(self.page)
        self.authorize_test_page()

    def test_link_profile(self) -> None:
        """Test the profile link."""
        self.test_page.click_link_profile()
        self.test_page.test_title(ProfilePage.title)

    @pytest.mark.filterwarnings('ignore')
    # Log out via GET requests is deprecated
    # https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings
    def test_link_logout(self) -> None:
        """Test the logout link."""
        self.test_page.click_link_logout()
        self.test_page.test_title(HomePage.title)

    def test_link_number(self) -> None:
        """Test link number."""
        expect(self.test_page.navbar).to_have_count(
            len(self.test_page.visible_logged)
        )


class TestNavbarAnonymous(TestNavbarMixin, POMTest):
    """Test navbar for anonymous."""

    __test__ = True

    def setUp(self) -> None:
        """Set up page data."""
        self.test_page = NavbarComponent(self.page)
        self.test_page.navigate(self.page_url)

    def test_link_registration(self) -> None:
        """Test the registration link."""
        self.test_page.click_link_registration()
        self.test_page.test_title(RegistrationPage.title)

    def test_link_login(self) -> None:
        """Test the login link."""
        self.test_page.click_link_login()
        self.test_page.test_title(LoginPage.title)

    def test_link_number(self) -> None:
        """Test link number."""
        expect(self.test_page.navbar).to_have_count(
            len(self.test_page.visible_anonymous)
        )
