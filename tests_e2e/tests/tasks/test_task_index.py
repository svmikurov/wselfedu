"""
Task index page module.
"""
from playwright.sync_api import expect

from tests_e2e.pages.tasks.index import IndexTaskPage
from tests_e2e.tests.base import POMBaseTest


class TestIndexTaskPage(POMBaseTest):
    """Test task index page class."""

    def setUp(self) -> None:
        """Set up task index page instance."""
        super().setUp()
        host = str(self.live_server_url)
        self.task_index = IndexTaskPage(self.page, host)
        self.task_index.navigate()

    def test_page_title(self) -> None:
        """Test task index page title."""
        self.task_index.test_title()

    def test_multiplication_table_btn(self) -> None:
        """Test multiplication table button."""
        expect(self.task_index.mult_table_btn).to_be_visible()
