"""Account application forms."""

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
)

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """User registration form."""

    class Meta:
        """Set form features."""

        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class CustomUserChangeForm(UserChangeForm):
    """Change user data form."""

    class Meta:
        """Set form features."""

        model = User
        fields = ('username',)
