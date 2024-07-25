from django.contrib.auth.forms import UserCreationForm

from users.models import UserModel


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

    def __init__(self, *args, **kwargs) -> None:
        """Add data-testid attr value to html tags."""
        super().__init__(*args, **kwargs)
        self.add_attr_for_field('username', {'data-testid': 'username'})
        self.add_attr_for_field('password1', {'data-testid': 'password1'})
        self.add_attr_for_field('password2', {'data-testid': 'password2'})

    def add_attr_for_field(
            self, field_name: str,
            data: dict[str, str],
    ) -> None:
        """Add attr with value to html representation field."""
        self.fields[field_name].widget.attrs.update(**data)

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')


class UserUpdateForm(UserRegistrationForm):
    """User update form."""

    def clean_username(self):
        """Enabling update data existing user.

        Override disables user uniqueness check.
        """
        return self.cleaned_data.get("username")
