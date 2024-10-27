"""User authentication views."""

from typing import Optional

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from contrib.views import FormMessageMixin


class UserLoginView(FormMessageMixin, LoginView):
    """User login view."""

    template_name = 'users/login.html'
    next_page = reverse_lazy('home')
    success_message = 'Вы вошли в приложение'


class UserLogoutView(FormMessageMixin, LogoutView):
    """User logout view."""

    next_page = reverse_lazy('home')
    success_message = 'Вы вышли из приложения'

    def get_default_redirect_url(self) -> Optional[str]:
        """Add success message."""
        messages.info(self.request, self.success_message)
        return super().get_default_redirect_url()
