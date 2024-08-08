"""Test mentorship profile page module."""

from playwright.sync_api import expect

from tests_e2e.pages.mentorship import MentorshipProfilePage
from tests_e2e.tests.base import POMTest, UserMixin


class TestMentorshipProfilePage(UserMixin, POMTest):
    """Test mentorship profile page."""

    student_name = 'student'
    mentor_name = 'mentor'

    @classmethod
    def setUpClass(cls) -> None:
        """Set up database data."""
        super().setUpClass()
        cls.student = cls.create_user(username=cls.student_name)
        cls.mentor = cls.create_user(username=cls.mentor_name)

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.test_page = MentorshipProfilePage(self.page, self.host)
        self.page_path = f'/users/mentorship/{self.student.pk}'
        self.authorize_test_page(username=self.student_name)
        self.test_page.navigate(url=self.page_url)

    def test_send_mentorship_request(self) -> None:
        """Test send mentorship request."""
        self.test_page.send_mentorship_request(mentor_name=self.mentor_name)
        expect(self.test_page.mentors_locator).to_contain_text(
            self.mentor_name
        )
