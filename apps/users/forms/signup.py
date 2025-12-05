"""Defines user sign up form."""

from django.contrib.auth.forms import UserCreationForm

from ..models import Person


class SignUpForm(UserCreationForm):  # type: ignore
    """User sign up form."""

    class Meta:
        """Configration of form."""

        model = Person
        fields = ('username', 'password1', 'password2')
