"""Test request, accept, and create mentorship module."""

from django.test import TestCase
from django.urls import reverse_lazy

from users.models import Mentorship, MentorshipRequest, UserModel


class TestRequestSendMentorship(TestCase):
    """Test send the request to mentorship."""

    @classmethod
    def setUpClass(cls):
        """Add users to database."""
        super().setUpClass()
        cls.student = UserModel.objects.create(username='student')
        cls.mentor = UserModel.objects.create(username='mentor')

    def test_send_mentorship_request(self):
        """Test send mentorship request."""
        self.url_send_mentorship_request = reverse_lazy(
            'users:send_mentorship_request',
            kwargs={'user_pk': self.student.pk},
        )
        self.client.force_login(self.student)

        self.client.post(
            self.url_send_mentorship_request,
            data={'input_mentor_name': self.mentor.username}
        )
        assert MentorshipRequest.objects.filter(
            from_user=self.student,
            to_user=self.mentor,
        ).exists() is True

    def test_send_twice_mentorship_request(self):
        """Test send request twice to the same user."""
        self.test_send_mentorship_request()
        self.test_send_mentorship_request()

        assert MentorshipRequest.objects.filter(
            from_user=self.student,
            to_user=self.mentor,
        ).count() == 1


class AcceptRequestToMentorship(TestCase):
    """Test accept the request to mentorship."""

    @classmethod
    def setUpClass(cls):
        """Add users to database."""
        super().setUpClass()
        cls.student = UserModel.objects.create(username='student')
        cls.mentor = UserModel.objects.create(username='mentor')

    def test_accept_mentorship_request(self):
        """Test accept mentorship request."""
        mentor_request = MentorshipRequest.objects.create(
            from_user=self.student, to_user=self.mentor,
        )
        url_accept_mentorship_request = reverse_lazy(
            'users:accept_mentorship_request',
            kwargs={'request_pk': mentor_request.pk},
        )
        self.client.force_login(self.mentor)

        self.client.post(url_accept_mentorship_request)

        assert Mentorship.objects.filter(
            mentor=self.mentor, student=self.student,
        ).exists() is True
