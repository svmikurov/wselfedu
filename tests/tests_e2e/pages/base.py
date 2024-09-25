"""The Page Object Model page base class module."""

from playwright.sync_api import Page, expect

SCREEN_PATH = 'tests_plw/screenshots/'


class BasePage:
    """Base class representing the page."""

    path = None
    host = None

    def __init__(self, page: Page) -> None:
        """Construct base page."""
        self.page = page

    @property
    def url(self) -> str:
        """Page url."""
        return self.host + self.path

    def navigate(
        self,
        *,
        host: str | None = None,
        url: str | None = None,
    ) -> None:
        """Navigate to page.

        Parameters
        ----------
        host : `str` | None, optional
            The page host for navigate (page host specified in the
            class representing the page, by default).
            Used to create the page URL.
        url : `str` | None, optional
            The page url for navigate (page url specified in the class
            representing the page, by default).

        """
        if url:
            page_url = url
        elif host:
            page_url = host + self.path
        else:
            page_url = self.url
        self.page.goto(page_url)


class BaseTests:
    """Common page tests class."""

    page: Page | None = None
    """Playwright Pyrest page fixture (`Page | None`).
    """
    title: str | None = None
    """Page title (`str | None`).
    """

    """Path to save page screenshot (`str`).
    """

    def test_title(self, expected_title: str | None = None) -> None:
        """Test page title.

        Parameters
        ----------
        expected_title : `str` | None, optional
            Expected page title (the value of the ``title`` attribute
            of the class representing the page, by default)

        """
        title = expected_title or self.title
        expect(self.page).to_have_title(title)

    def take_screen(self, file_name: str) -> None:
        """Take a page screenshot."""
        path = f'{SCREEN_PATH}{file_name}.png'
        self.page.screenshot(path=path)


class POMPage(BasePage, BaseTests):
    """Class representing the testing page with general tests."""
