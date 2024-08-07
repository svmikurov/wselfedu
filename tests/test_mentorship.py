"""Test request, accept, delete and create views mentorship module."""

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from contrib.tests_extension import flash_message_test
from users.models import Mentorship, MentorshipRequest, UserModel


class MentorshipTestMixin(TestCase):
    """Mentorship test base class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.student = UserModel.objects.create(username='student')
        cls.mentor = UserModel.objects.create(username='mentor')
        cls.other_user = UserModel.objects.create(username='other_user')

    @property
    def is_exists_mentorship_request(self) -> bool:
        """Is exists mentorship request (`bool`, reade-only)."""
        return MentorshipRequest.objects.filter(
            from_user=self.student, to_user=self.mentor
        ).exists()

    @property
    def is_exists_mentorship(self) -> bool:
        """Is exists mentorship (`bool`, reade-only)."""
        return Mentorship.objects.filter(
            student=self.student, mentor=self.mentor
        ).exists()


class TestSendMentorshipRequestView(MentorshipTestMixin, TestCase):
    """Test send the request to mentorship view."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.url_send_mentorship_request = reverse_lazy(
            'users:send_mentorship_request',
            kwargs={'user_pk': cls.student.pk},
        )
        cls.request_mentor_data = {'input_mentor_name': cls.mentor.username}

    def test_send_mentorship_request_by_student(self) -> None:
        """Send request to mentorship by student."""
        self.client.force_login(self.student)
        send_request_once_msg = (
            f'Заявка на добавление ментора '
            f'отправлена {self.mentor.username}'
        )
        send_request_twice_msg = (
            f'Заявка на добавление ментора '
            f'уже была отправлена {self.mentor.username}'
        )

        self.client.post(
            self.url_send_mentorship_request,
            self.request_mentor_data,
        )
        # second request to the mentor
        response = self.client.post(
            self.url_send_mentorship_request,
            self.request_mentor_data,
        )
        storage = get_messages(response.wsgi_request)
        first_msg, second_msg = storage

        assert str(first_msg) == send_request_once_msg
        assert str(second_msg) == send_request_twice_msg
        # a record of request to mentorship in database is unique
        mentorship_request = MentorshipRequest.objects.filter(
            from_user=self.student,
            to_user=self.mentor,
        ).count()
        assert mentorship_request == 1

    def test_send_mentorship_request_to_non_existent_user(self) -> None:
        """Send request to mentorship to non-existent user."""
        msg = 'Пользователь с именем non-existent user не зарегистрирован'
        self.client.force_login(self.student)
        response = self.client.post(
            self.url_send_mentorship_request,
            {'input_mentor_name': 'non-existent user'},
        )
        assert self.is_exists_mentorship_request is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_send_mentorship_request_by_mentor(self) -> None:
        """Send request to mentorship by mentor."""
        msg = 'Пользователь не может стать своим наставником'
        self.client.force_login(self.mentor)
        response = self.client.post(
            self.url_send_mentorship_request, self.request_mentor_data
        )
        assert self.is_exists_mentorship_request is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_send_mentorship_request_by_anonymous(self) -> None:
        """Send request to mentorship by anonymous."""
        self.client.post(
            self.url_send_mentorship_request, self.request_mentor_data
        )
        assert self.is_exists_mentorship_request is False


class TestDeleteMentorshipRequestView(MentorshipTestMixin, TestCase):
    """Test delete the request to mentorship view."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.mentorship_request = MentorshipRequest.objects.create(
            from_user=cls.student, to_user=cls.mentor
        )
        cls.delete_url = reverse_lazy(
            'users:delete_mentorship_request',
            kwargs={'pk': cls.mentorship_request.pk},
        )

    def test_delete_mentorship_request_by_student(self) -> None:
        """Test delete by student the mentorship request."""
        msg = 'Запрос удален'
        self.client.force_login(self.student)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is False
        flash_message_test(response, msg)

    def test_delete_mentorship_request_by_mentor(self) -> None:
        """Test delete by mentor the mentorship request."""
        msg = 'Запрос удален'
        self.client.force_login(self.mentor)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is False
        flash_message_test(response, msg)

    def test_delete_mentorship_request_by_other_user(self) -> None:
        """Test delete by other user the mentorship request."""
        msg = 'Для доступа необходимо войти в приложение'
        self.client.force_login(self.other_user)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is True
        flash_message_test(response, msg)

    def test_delete_mentorship_request_by_anonymous(self) -> None:
        """Test delete by anonymous the mentorship request."""
        msg = 'Для доступа необходимо войти в приложение'
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is True
        flash_message_test(response, msg)


class TestDeleteMentorshipView(MentorshipTestMixin, TestCase):
    """Test delete mentorship view."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.mentorship = Mentorship.objects.create(
            student=cls.student, mentor=cls.mentor
        )
        cls.delete_mentorship_url = reverse_lazy(
            'users:delete_mentorship', kwargs={'pk': cls.mentorship.pk}
        )

    def test_delete_mentorship_by_student(self) -> None:
        """Test delete mentorship by student."""
        msg = 'Наставничество удалено'
        self.client.force_login(self.student)
        response = self.client.post(self.delete_mentorship_url)

        assert self.is_exists_mentorship is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_delete_mentorship_by_mentor(self) -> None:
        """Test delete mentorship by mentor."""
        msg = 'Наставничество удалено'
        self.client.force_login(self.mentor)
        response = self.client.post(self.delete_mentorship_url)

        assert self.is_exists_mentorship is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_delete_mentorship_by_other_user(self) -> None:
        """Test delete mentorship by other user."""
        msg = 'Для доступа необходимо войти в приложение'
        self.client.force_login(self.other_user)
        response = self.client.post(self.delete_mentorship_url)

        assert self.is_exists_mentorship is True
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_delete_mentorship_by_anonymous(self) -> None:
        """Test delete mentorship by other anonymous."""
        msg = 'Для доступа необходимо войти в приложение'
        response = self.client.post(self.delete_mentorship_url)

        assert self.is_exists_mentorship is True
        assert str(*get_messages(response.wsgi_request)) == msg


class AcceptRequestToMentorship(MentorshipTestMixin, TestCase):
    """Test accept the request to mentorship."""

    @classmethod
    def setUpClass(cls):
        """Add users to database."""
        super().setUpClass()
        cls.mentor_request = MentorshipRequest.objects.create(
            from_user=cls.student, to_user=cls.mentor
        )
        cls.url_accept_mentorship_request = reverse_lazy(
            'users:accept_mentorship_request',
            kwargs={'request_pk': cls.mentor_request.pk},
        )

    def test_accept_mentorship_request_by_mentor(self):
        """Test access mentorship request by mentor."""
        msg = 'Вы стали наставником student'
        self.client.force_login(self.mentor)
        response = self.client.post(self.url_accept_mentorship_request)

        assert self.is_exists_mentorship is True
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_accept_mentorship_request_by_student(self) -> None:
        """Test access mentorship request by mentor."""
        msg = 'Вы не можете стать наставником'
        self.client.force_login(self.student)
        response = self.client.post(self.url_accept_mentorship_request)

        assert self.is_exists_mentorship is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_accept_mentorship_request_by_other_user(self) -> None:
        """Test access mentorship request by other user."""
        msg = 'Вы не можете стать наставником'
        self.client.force_login(self.other_user)
        response = self.client.post(self.url_accept_mentorship_request)

        assert self.is_exists_mentorship is False
        assert str(*get_messages(response.wsgi_request)) == msg

    def test_accept_mentorship_request_by_anonymous(self) -> None:
        """Test access mentorship request by anonymous."""
        self.client.post(self.url_accept_mentorship_request)
        assert self.is_exists_mentorship is False
