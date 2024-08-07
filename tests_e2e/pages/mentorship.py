"""Mentorship profile page representation module."""

from typing import Optional

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class MentorshipProfilePage(POMPage):
    """Mentorship page representation class."""

    title = 'Наставничество'

    def __init__(self, page: Page, host: Optional[str] = None) -> None:
        """Construct page."""
        super().__init__(page)
        self.page = page
        self.host = host

        self.mentor_name_input = page.get_by_placeholder(
            'Введите имя наставника'
        )
        self.request_btn = page.get_by_role('button', name='Добавить')
        self.refuse_btn = page.get_by_role('button', name='Отказаться')
        self.recall_btn = page.get_by_role('button', name='Отозвать')
        self.reject_btn = page.get_by_role('button', name='Отклонить')

        self.mentors_locator = self.page.get_by_test_id('mentors')
        self.students_locator = self.page.get_by_test_id('students')
        self.got_requests_locator = self.page.get_by_test_id('got_requests')
        self.sent_requests_locator = self.page.get_by_test_id('sent_requests')

    def send_mentorship_request(self, mentor_name: str) -> None:
        """Send mentorship request."""
        self.mentor_name_input.fill(mentor_name)
        self.request_btn.click()

    def delete_mentorship_request_by_student(self) -> None:
        """Delete mentorship request by student."""

    def accept_mentorship_request(self) -> None:
        """Accept mentorship request by mentor."""

    def refuse_mentorship_request(self) -> None:
        """Decline mentorship request by mentor."""

    def delete_mentorship_by_student(self) -> None:
        """Delete mentorship bu student."""

    def delete_mentorship_by_mentor(self) -> None:
        """Delete mentorship bu mentor."""
