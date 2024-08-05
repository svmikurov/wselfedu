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
            data={'input_mentor_name': self.mentor.username},
        )
        assert (
            MentorshipRequest.objects.filter(
                from_user=self.student,
                to_user=self.mentor,
            ).exists()
            is True
        )

    def test_send_twice_mentorship_request(self):
        """Test send request twice to the same user."""
        self.test_send_mentorship_request()
        self.test_send_mentorship_request()

        mentorship_request = MentorshipRequest.objects.filter(
            from_user=self.student,
            to_user=self.mentor,
        ).count()
        assert mentorship_request == 1


class AcceptRequestToMentorship(TestCase):
    """Test accept the request to mentorship."""

    @classmethod
    def setUpClass(cls):
        """Add users to database."""
        super().setUpClass()
        cls.student = UserModel.objects.create(username='student')
        cls.mentor = UserModel.objects.create(username='mentor')
        cls.mentor_request = MentorshipRequest.objects.create(
            from_user=cls.student,
            to_user=cls.mentor,
        )
        cls.url_accept_mentorship_request = reverse_lazy(
            'users:accept_mentorship_request',
            kwargs={'request_pk': cls.mentor_request.pk},
        )

    def test_accept_mentorship_request(self):
        """Test accept mentorship request."""
        self.client.force_login(self.mentor)
        self.client.post(self.url_accept_mentorship_request)

        mentorship = Mentorship.objects.filter(
            mentor=self.mentor,
            student=self.student,
        ).exists()
        assert mentorship is True


class TestDeleteMentorshipByMentor(TestCase):
    """Test delete mentorship by mentor."""

    @classmethod
    def setUpClass(cls):
        """Setup test data."""
        super().setUpClass()
        cls.user = UserModel.objects.create(username='user')
        cls.mentor = UserModel.objects.create(username='mentor')
        cls.student = UserModel.objects.create(username='student')
        cls.profile_url = reverse_lazy(
            'users:detail',
            kwargs={'pk': cls.mentor.pk},
        )
        cls.mentorship = Mentorship.objects.create(
            mentor=cls.mentor,
            student=cls.student,
        )
        cls.mentorship_request = MentorshipRequest.objects.create(
            to_user=cls.mentor,
            from_user=cls.student,
        )

    def test_profile_context(self):
        """Test profile context contains data."""
        self.client.force_login(self.mentor)
        response = self.client.get(self.profile_url)

        context_mentorship_pk = (
            response.context.get('mentorship_students').last().get('id')
        )
        assert context_mentorship_pk == self.mentorship.pk

    def test_delete_mentorship_request_by_mentor(self):
        """Test delete mentorship by mentor."""
        self.client.force_login(self.mentor)
        self.client.post(
            reverse_lazy(
                'users:delete_mentorship_request_by_mentor',
                kwargs={'pk': self.mentorship_request.pk},
            )
        )
        mentorship_request = MentorshipRequest.objects.filter(
            pk=self.mentorship_request.pk
        ).exists()
        assert mentorship_request is False

    def test_delete_mentorship_request_by_student(self):
        """Test delete mentorship by mentor."""
        self.client.force_login(self.student)
        self.client.post(
            reverse_lazy(
                'users:delete_mentorship_request_by_student',
                kwargs={'pk': self.mentorship_request.pk},
            )
        )
        mentorship_request = MentorshipRequest.objects.filter(
            pk=self.mentorship_request.pk
        ).exists()
        assert mentorship_request is False

    def test_delete_mentorship_by_mentor(self):
        """Test delete mentorship by mentor."""
        self.client.force_login(self.mentor)
        self.client.post(
            reverse_lazy(
                'users:delete_mentorship_by_mentor',
                kwargs={'pk': self.mentorship.pk},
            )
        )
        assert (
            Mentorship.objects.filter(pk=self.mentorship.pk).exists() is False
        )

    def test_delete_mentorship_by_student(self):
        """Test delete mentorship by student."""
        self.client.force_login(self.student)
        self.client.post(
            reverse_lazy(
                'users:delete_mentorship_by_student',
                kwargs={'pk': self.mentorship.pk},
            )
        )
        assert (
            Mentorship.objects.filter(pk=self.mentorship.pk).exists() is False
        )
