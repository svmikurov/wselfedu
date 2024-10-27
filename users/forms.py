"""User application forms."""

from captcha.fields import CaptchaField
from django.contrib.auth.forms import UserCreationForm

from config.constants import DATA_TESTID, USERNAME
from users.models import UserApp


class UserRegistrationForm(UserCreationForm):
    """User registration form."""

    captcha = CaptchaField()

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Add "data-testid" attr value to html tags of form."""
        super().__init__(*args, **kwargs)
        self.add_attr_for_field(USERNAME, {DATA_TESTID: USERNAME})
        self.add_attr_for_field('password1', {DATA_TESTID: 'password1'})
        self.add_attr_for_field('password2', {DATA_TESTID: 'password2'})

    def add_attr_for_field(
        self,
        field_name: str,
        data: dict[str, str],
    ) -> None:
        """Add attr with value to html tags of form."""
        self.fields[field_name].widget.attrs.update(**data)

    class Meta:
        """Set model features."""

        model = UserApp
        fields = (USERNAME, 'password1', 'password2')


class UserUpdateForm(UserRegistrationForm):
    """User update form."""

    def clean_username(self) -> str:
        """Allow updating existing user data.

        Override disables user uniqueness check.
        """
        return self.cleaned_data.get(USERNAME)
