"""E2E test profile page module.

Testing using the :obj:`ProfilePage
<tests_plw.pages.profile.ProfilePage>`
page representation class.
"""

from playwright.sync_api import expect

from tests_plw.pages import (
    MathCalculateExercisePage,
)
from tests_plw.pages.profile import ProfilePage
from tests_plw.tests.base import POMTest


class TestProfile(POMTest):
    """Test profile page."""

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.authorize_test_page()
        self.test_page = ProfilePage(self.page)
        self.page_path = f'/users/{self.user.pk}/account'
        self.test_page.navigate(page_url=self.page_url)

    def test_mult_table_page_btn(self) -> None:
        """Test click button for start Table mult exercise."""
        self.test_page.start_study_mult_table()
        self.test_page.test_title(MathCalculateExercisePage.title)

    def test_page_content(self) -> None:
        """Test user pofile page content.

        .. admonition:: Test what the page contains

            * Username

        """
        # The user profile page contains the text of the username.
        expect(self.test_page.page.get_by_text(self.username)).to_be_visible()
