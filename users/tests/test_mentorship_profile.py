"""Test user mentorship profile views module."""

from django.test import TestCase
from django.urls import reverse_lazy

from config.constants import MENTOR, PK, STUDENT
from users.models import Mentorship, UserApp


class TestMentorshipPage(TestCase):
    """Test the access to the user mentorship profile."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up tes data."""
        super().setUpClass()
        cls.student = UserApp.objects.create(username=STUDENT)
        cls.mentor = UserApp.objects.create(username=MENTOR)
        cls.other_user = UserApp.objects.create(username='other_user')
        cls.mentorship = Mentorship.objects.create(
            student=cls.student, mentor=cls.mentor
        )
        cls.mentorship_profile_url = reverse_lazy(
            'users:mentorship_profile', kwargs={PK: cls.student.pk}
        )

    def test_student_access(self) -> None:
        """Test the student access to page."""
        self.client.force_login(self.student)
        response = self.client.get(self.mentorship_profile_url)
        self.assertEqual(response.status_code, 200)

    def test_mentor_access(self) -> None:
        """Test the mentor access to page."""
        self.client.force_login(self.mentor)
        response = self.client.get(self.mentorship_profile_url)
        self.assertEqual(response.status_code, 302)

    def test_other_user_access(self) -> None:
        """Test the other user access to page."""
        self.client.force_login(self.other_user)
        response = self.client.get(self.mentorship_profile_url)
        self.assertEqual(response.status_code, 302)
