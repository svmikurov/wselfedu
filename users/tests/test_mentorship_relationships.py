"""Test request, accept, delete and create views mentorship module."""

from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from contrib.tests.extension import flash_message_test
from users.models import Mentorship, MentorshipRequest, UserApp


class MentorshipTestMixin(TestCase):
    """Mentorship test mixin."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up test data."""
        super().setUpClass()
        cls.student = UserApp.objects.create(username='student')
        cls.mentor = UserApp.objects.create(username='mentor')
        cls.other_user = UserApp.objects.create(username='other_user')
        cls.success_redirect_url = reverse_lazy(
            'users:mentorship_profile', kwargs={'pk': cls.student.pk}
        )

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
        msg = f'Заявка отправлена {self.mentor.username}'
        msg_wrong = f'Заявка уже была отправлена {self.mentor.username}'

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

        assert str(first_msg) == msg
        assert str(second_msg) == msg_wrong
        # a record of request to mentorship in database is unique
        mentorship_request = MentorshipRequest.objects.filter(
            from_user=self.student,
            to_user=self.mentor,
        ).count()
        assert mentorship_request == 1
        self.assertRedirects(
            response, self.success_redirect_url, HTTPStatus.FOUND
        )

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
        self.assertRedirects(
            response, self.success_redirect_url, HTTPStatus.FOUND
        )

    def test_send_mentorship_request_to_mentor(self) -> None:
        """Send request the mentorship to already assigned mentor."""
        Mentorship.objects.create(mentor=self.mentor, student=self.student)
        msg = 'Запрашиваемый пользователь уже ваш наставник'
        self.client.force_login(self.student)
        response = self.client.post(
            self.url_send_mentorship_request, self.request_mentor_data
        )
        assert self.is_exists_mentorship_request is False
        assert str(*get_messages(response.wsgi_request)) == msg
        self.assertRedirects(
            response, self.success_redirect_url, HTTPStatus.FOUND
        )

    def test_send_mentorship_request_by_mentor(self) -> None:
        """Send request to mentorship by student to itself."""
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
        """Test to delete the mentorship request by student."""
        msg = 'Запрос удален'
        self.client.force_login(self.student)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is False
        flash_message_test(response, msg)
        self.assertRedirects(
            response, self.success_redirect_url, HTTPStatus.FOUND
        )

    def test_delete_mentorship_request_by_mentor(self) -> None:
        """Test to delete the mentorship request by mentor."""
        msg = 'Запрос удален'
        self.client.force_login(self.mentor)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is False
        flash_message_test(response, msg)

    def test_delete_mentorship_request_by_other_user(self) -> None:
        """Test to delete the mentorship request by other user."""
        msg = 'Для доступа необходимо войти в приложение'
        self.client.force_login(self.other_user)
        response = self.client.post(self.delete_url)

        assert self.is_exists_mentorship_request is True
        flash_message_test(response, msg)

    def test_delete_mentorship_request_by_anonymous(self) -> None:
        """Test to delete the mentorship request by anonymous."""
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
        self.assertRedirects(
            response, self.success_redirect_url, HTTPStatus.FOUND
        )

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
    def setUpClass(cls) -> None:
        """Add users to database."""
        super().setUpClass()
        cls.mentor_request = MentorshipRequest.objects.create(
            from_user=cls.student, to_user=cls.mentor
        )
        cls.url_accept_mentorship_request = reverse_lazy(
            'users:accept_mentorship_request',
            kwargs={'request_pk': cls.mentor_request.pk},
        )

    def test_accept_mentorship_request_by_mentor(self) -> None:
        """Test access mentorship request by mentor."""
        msg = 'Вы стали наставником student'
        success_redirect_url = reverse_lazy(
            'users:mentorship_profile', kwargs={'pk': self.mentor.pk}
        )
        self.client.force_login(self.mentor)
        response = self.client.post(self.url_accept_mentorship_request)

        assert self.is_exists_mentorship is True
        assert str(*get_messages(response.wsgi_request)) == msg
        self.assertRedirects(response, success_redirect_url, HTTPStatus.FOUND)

    def test_accept_mentorship_request_by_student(self) -> None:
        """Test access mentorship request by student."""
        self.client.force_login(self.student)
        self.client.post(self.url_accept_mentorship_request)
        assert self.is_exists_mentorship is False

    def test_accept_mentorship_request_by_other_user(self) -> None:
        """Test access mentorship request by other user."""
        self.client.force_login(self.other_user)
        self.client.post(self.url_accept_mentorship_request)
        assert self.is_exists_mentorship is False

    def test_accept_mentorship_request_by_anonymous(self) -> None:
        """Test access mentorship request by anonymous."""
        self.client.post(self.url_accept_mentorship_request)
        assert self.is_exists_mentorship is False
