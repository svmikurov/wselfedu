from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from contrib_app.mixins import AddMessageToFormSubmissionMixin


class UserLoginView(
    AddMessageToFormSubmissionMixin,
    LoginView,
):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Вход в приложение',
    }
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
