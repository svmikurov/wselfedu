"""Defines user sign up form."""

from django.contrib.auth.forms import UserCreationForm

from ..models import CustomUser


class SignUpForm(UserCreationForm):  # type: ignore[type-arg]
    """User sign up form."""

    class Meta:
        """Configration of form."""

        model = CustomUser
        fields = ('username', 'password1', 'password2')
