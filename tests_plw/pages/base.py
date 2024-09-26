"""Base POM page.

Inherit your test page representation classes from POMPage.

.. _pom_page_example:

Example
-------
.. code-block:: python

    from tests_plw.pages.base import POMPage

    class MentorshipProfilePage(POMPage):

    title = 'Profile'

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

from typing import Optional

from playwright.sync_api import Page, Response, expect

SCREENSHOT_DIR = 'tests_plw/screenshots/'
"""Path to save page screenshot (`str`).
"""


class BasePage:
    """Base page of Page Object Model.

    :param Page page: Playwright Pytest page fixture.
    """

    title = None
    """Page title (`Optional[str]`).
    """
    path: Optional[str]
    """Url schema path to page (`Optional[str]`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        self.page = page
        self.path = None

    def navigate(self, page_url: str) -> Response:
        """Navigate to page.

        :param str page_url: The page url for navigate.
        :return: Returns the main resource response.
        :rtype: Response
        """
        response = self.page.goto(page_url)
        return response


class BaseTestMixin:
    """Common page tests class."""

    page: Page
    """Playwright Pytest page fixture (`Page`)
    """
    title: Optional[str]
    """Page title (`Optional[str]`).
    """

    def test_title(self, expected_title: Optional[str] = None) -> None:
        """Test page title.

        :param `Optional[str]` expected_title: Expected page title (the
         value of the ``title`` attribute of the class representing the
         page, by default)

        Examples
        --------
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

        :param str file_name: File name to save screenshot.

        Example
        -------
        .. code-block:: python

           self.test_page.take_screen(file_name='completed_form')

        """
        screenshot_path = f'{SCREENSHOT_DIR}{file_name}.png'
        self.page.screenshot(path=screenshot_path)


class POMPage(BasePage, BaseTestMixin):
    """Class representing the testing page with general tests."""
