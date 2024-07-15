from playwright.sync_api import Page, expect


class BasePage:
    """Base class representing the page."""

    host: str
    path: str

    def __init__(self, page: Page):
        self.page = page

    @property
    def url(self) -> str:
        """Page url."""
        return self.host + self.path

    def navigate(self, url=None) -> None:
        """Navigate to page.

        Parameters
        ----------
        url : `str`, optional
            The page url for navigate (page url specified in the class
            representing the page, by default)
        """
        page_url = url or self.url
        self.page.goto(page_url)


class BaseTests:
    """Common page tests class."""

    page: Page
    title: str

    def test_title(self, expected_title=None):
        """Test page title.

        Parameters
        ----------
        expected_title : `str`, optional
            Expected page title (The value of the ``title`` attribute
            of the class representing the page, by default)
        """
        title = expected_title or self.title
        expect(self.page).to_have_title(title)


class TestPage(BasePage, BaseTests):
    """Base class representing the testing page with general tests."""
