"""Defines user application forms."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):  # type: ignore[type-arg]
    """User sign up form."""

    class Meta:
        """Configure the form."""

        model = get_user_model()
        fields = ('username', 'password1', 'password2')
