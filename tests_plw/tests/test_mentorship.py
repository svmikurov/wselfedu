"""Test mentorship profile page module.

Testing using the :obj:`Mentorship page <tests_plw.pages.mentorship>`
page representation class.

Test authorized page.

.. admonition:: Testing page elements

    **class MentorshipProfilePageElementsTest:**

    * Page title

.. admonition:: Testing page features

    **class MentorshipStudentProfilePageTest:**

    * Test send mentorship request
    * Test delete mentorship request by student
    * Test delete mentorship by student

    **class MentorshipMentorProfilePageTest:**

    * Test accept mentorship request by mentor
    * Test refuse mentorship request by mentor
    * Test delete mentorship by mentor

"""

from playwright.sync_api import expect

from tests_plw.pages.mentorship import MentorshipProfilePage
from tests_plw.tests.base import POMTest
from users.models import Mentorship, MentorshipRequest


class MentorshipProfilePageTest(POMTest):
    """Test mentorship profile page."""

    student_name = 'student'
    mentor_name = 'mentor'

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.student = self.create_user(username=self.student_name)
        self.mentor = self.create_user(username=self.mentor_name)
        self.test_page = MentorshipProfilePage(self.page)

    def add_mentorship_request_to_database(self) -> None:
        """Add mentorship request to database."""
        MentorshipRequest.objects.create(
            from_user=self.student, to_user=self.mentor
        )
        self.test_page.navigate(page_url=self.page_url)

    def add_mentorship_to_database(self) -> None:
        """Add mentorship to database."""
        Mentorship.objects.create(student=self.student, mentor=self.mentor)
        self.test_page.navigate(page_url=self.page_url)


class MentorshipProfilePageElementsTest(MentorshipProfilePageTest):
    """Test mentorship profile page elements."""

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.authorize_test_page(user=self.student)
        self.page_path = f'/users/mentorship/{self.student.pk}'
        self.test_page.navigate(page_url=self.page_url)

    def test_title(self) -> None:
        """Test page title."""
        self.test_page.test_title()


class MentorshipStudentProfilePageTest(MentorshipProfilePageTest):
    """Test mentorship student profile page."""

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.authorize_test_page(user=self.student)
        self.page_path = f'/users/mentorship/{self.student.pk}'

    def test_send_mentorship_request(self) -> None:
        """Test send mentorship request."""
        self.test_page.navigate(page_url=self.page_url)
        self.test_page.send_mentorship_request(mentor_name=self.mentor_name)
        expect(self.test_page.sent_requests).to_contain_text(self.mentor_name)

    def test_delete_mentorship_request_by_student(self) -> None:
        """Test delete mentorship request by student."""
        self.add_mentorship_request_to_database()
        self.test_page.delete_mentorship_request_by_student()
        expect(self.test_page.sent_requests).not_to_contain_text(
            self.mentor_name,
        )

    def test_delete_mentorship_by_student(self) -> None:
        """Test delete mentorship by student."""
        self.add_mentorship_to_database()
        self.test_page.delete_mentorship_by_student()
        expect(self.test_page.mentors).not_to_contain_text(self.mentor_name)


class MentorshipMentorProfilePageTest(MentorshipProfilePageTest):
    """Test mentorship mentor profile page."""

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.authorize_test_page(user=self.mentor)
        self.page_path = f'/users/mentorship/{self.mentor.pk}'

    def test_accept_mentorship_request(self) -> None:
        """Test accept mentorship request by mentor."""
        self.add_mentorship_request_to_database()
        expect(self.test_page.got_requests).to_contain_text(self.student_name)
        self.test_page.accept_mentorship_request_by_mentor()
        expect(self.test_page.got_requests).not_to_contain_text(
            self.student_name,
        )
        expect(self.test_page.students).to_contain_text(self.student_name)

    def test_refuse_mentorship_request(self) -> None:
        """Test refuse mentorship request by mentor."""
        self.add_mentorship_request_to_database()
        expect(self.test_page.got_requests).to_contain_text(self.student_name)
        self.test_page.reject_mentorship_request_by_mentor()
        expect(self.test_page.got_requests).not_to_contain_text(
            self.student_name,
        )
        expect(self.test_page.students).not_to_contain_text(self.student_name)

    def test_delete_mentorship_by_mentor(self) -> None:
        """Test delete mentorship by mentor."""
        self.add_mentorship_to_database()
        expect(self.test_page.students).to_contain_text(self.student_name)
        self.test_page.delete_mentorship_by_mentor()
        expect(self.test_page.students).not_to_contain_text(self.student_name)
