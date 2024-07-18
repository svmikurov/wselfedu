from playwright.sync_api import Page, expect


class BasePage:
    """Base class representing the page."""

    host: str
    path: str

    def __init__(self, page: Page) -> None:
        """Page constructor."""
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

    page: Page
    title: str

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


class TestPage(BasePage, BaseTests):
    """Base class representing the testing page with general tests."""
