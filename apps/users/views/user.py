"""Defines user CRUD models."""

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import SignUpForm  # type: ignore


class SignUpView(CreateView):  # type: ignore[type-arg]
    """User sign up view."""

    model = get_user_model()
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
