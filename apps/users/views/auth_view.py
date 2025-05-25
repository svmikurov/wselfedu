"""Defines user registration and authentication views."""

from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..forms import CustomUserCreationForm


class SignUpView(CreateView):
    """User registration view."""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
