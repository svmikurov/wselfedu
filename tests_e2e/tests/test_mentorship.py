"""Test mentorship profile page module."""

from urllib.parse import urljoin

from playwright.sync_api import expect

from tests_e2e.pages.mentorship import MentorshipProfilePage
from tests_e2e.tests.base import POMTest, UserMixin


class TestMentorshipProfilePage(UserMixin, POMTest):
    """Test mentorship profile page."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up database data."""
        super().setUpClass()
        cls.student = cls.create_user(username='student')
        cls.mentor = cls.create_user(username='mentor')

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.test_page = MentorshipProfilePage(self.page, self.host)
        self.path = f'/users/mentorship/{self.student.pk}'
        self.authorize_test_page(username='student')
        self.test_page.navigate(url=self.url)

    def test_send_mentorship_request(self) -> None:
        """Test send mentorship request."""
        self.test_page.send_mentorship_request(mentor_name='mentor')
        expect(self.test_page.mentors_locator).to_contain_text('mentor')
