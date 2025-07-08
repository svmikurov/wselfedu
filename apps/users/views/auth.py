"""Defines authentication views."""

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.forms import SignUpForm


class SignUpView(CreateView):  # type: ignore[type-arg]
    """User sign up view."""

    model = get_user_model()
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
