from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from contrib_app.mixins import AddMessageToFormSubmissionMixin
from users.forms import UserRegistrationForm


class UserRegistrationView(AddMessageToFormSubmissionMixin, CreateView):
    """
    User registration in the application.
    """
    form_class = UserRegistrationForm
    extra_context = {
        'title': 'Регистрация',
        'btn_name': 'Зарегистрироваться',
    }
    success_url = reverse_lazy('users:login')
    success_message = 'Вы зарегистрировались'


class UserLoginView(
    AddMessageToFormSubmissionMixin,
    LoginView,
):
    next_page = reverse_lazy('home')
    success_message = 'Вы вошли в приложение'


class UserLogoutView(
    AddMessageToFormSubmissionMixin,
    LogoutView,
):
    next_page = reverse_lazy('home')
    success_message = 'Вы вышли из приложения'

    def get_default_redirect_url(self):
        messages.info(self.request, self.success_message)
        return super().get_default_redirect_url()
