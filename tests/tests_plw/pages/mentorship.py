"""Mentorship profile page representation module."""

from playwright.sync_api import Page

from tests.tests_plw.pages.base import POMPage


class MentorshipProfilePage(POMPage):
    """Mentorship page representation class.

    Parameters
    ----------
    page : `Page`
        Playwright Pytest page fixture.

    """

    title = 'Наставничество'
    """Page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct page."""
        super().__init__(page)
        self.page = page

        self.mentors = page.get_by_test_id('mentors')
        self.students = page.get_by_test_id('students')
        self.got_requests = page.get_by_test_id('got_requests')
        self.sent_requests = page.get_by_test_id('sent_requests')

        self.mentor_name_input = page.get_by_placeholder(
            'Введите имя наставника'
        )
        self.request_btn = page.get_by_role('button', name='Добавить')
        self.refuse_btn = page.get_by_role('button', name='Отказаться')
        self.recall_btn = page.get_by_role('button', name='Отозвать')
        self.accept_btn = page.get_by_role('button', name='Принять')
        self.reject_btn = page.get_by_role('button', name='Отклонить')

    def send_mentorship_request(self, mentor_name: str) -> None:
        """Send mentorship request.

        Parameters
        ----------
        mentor_name : `str`
            The user to whom the mentoring request is sent.

        """
        self.mentor_name_input.fill(mentor_name)
        self.request_btn.click()

    def delete_mentorship_request_by_student(self) -> None:
        """Delete mentorship request by student."""
        self.recall_btn.click()

    def delete_mentorship_by_student(self) -> None:
        """Delete mentorship bu student."""
        self.refuse_btn.click()

    def accept_mentorship_request_by_mentor(self) -> None:
        """Accept mentorship request by mentor."""
        self.accept_btn.click()

    def reject_mentorship_request_by_mentor(self) -> None:
        """Refuse mentorship request by mentor."""
        self.reject_btn.click()

    def delete_mentorship_by_mentor(self) -> None:
        """Delete mentorship bu mentor."""
        self.refuse_btn.click()
