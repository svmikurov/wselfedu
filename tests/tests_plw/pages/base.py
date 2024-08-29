"""The Page Object Model module of base page."""

from typing import Optional

from playwright.sync_api import Page, expect


class BasePage:
    """Base page of Page Object Model.

    Parameters
    ----------
    page : `Page`
        Playwright Pytest page fixture.

    """

    title = None
    """Page title (`Optional[str]`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        self.page = page

    def navigate(self, page_url: str) -> None:
        """Navigate to page.

        Parameters
        ----------
        page_url : `str`
            The page url for navigate.

        """
        self.page.goto(page_url)


class BaseTestMixin:
    """Common page tests class."""

    page: Page
    """Playwright Pytest page fixture (`Page`)
    """
    title = None
    """Page title (`Optional[str]`).
    """
    screenshot_dir = 'tests/tests_plw/screenshots/'
    """Path to save page screenshot (`str`).
    """

    def test_title(self, expected_title: Optional[str] = None) -> None:
        """Test page title.

        Parameters
        ----------
        expected_title : `Optional[str]`, optional
            Expected page title (the value of the ``title`` attribute
            of the class representing the page, by default)

        Example
        -------
        Test some page title:

        .. code-block:: python

           self.test_page.test_title()

        Test the title of another page:

        .. code-block:: python

           from pages.home import HomePage

           self.test_page.test_title(expected_title=HomePage.title)

        """
        title = expected_title or self.title
        expect(self.page).to_have_title(title)

    def take_screen(self, file_name: str) -> None:
        """Take a page screenshot.

        Parameters
        ----------
        file_name : `str`
            File name to save screenshot.

        Example
        -------
        .. code-block:: python

           self.test_page.take_screen(file_name='completed_form')

        """
        screenshot_path = f'{self.screenshot_dir}{file_name}.png'
        self.page.screenshot(path=screenshot_path)


class POMPage(
    BasePage,
    BaseTestMixin,
):
    """Class representing the testing page with general tests.

    Inherit your page classes from this class.

    .. _pom_page_example:

    Example
    -------
    .. code-block:: python

        class MentorshipProfilePage(POMPage):

        title = 'Профиль'

        def __init__(self, page: Page) -> None:
            super().__init__(page)
            self.page = page

            self.one = page.get_by_role('button', name='one')
            self.two = page.get_by_role('button', name='two')

            self.locator_one = page.get_by_text('one')
            self.locator_two = page.get_by_text('two')

        def do_one(self) -> None:
            self.one.click()

        def do_two(self) -> None:
            self.two.click()

    """
