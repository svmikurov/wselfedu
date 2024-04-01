from django.contrib.auth.forms import UserCreationForm

from users.models import UserModel


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'data-test': 'username'}
        )
        self.fields['username'].widget.attrs.update(
            {'data-test': 'password1'}
        )
        self.fields['username'].widget.attrs.update(
            {'data-test': 'password2'}
        )


class UserUpdateForm(UserRegistrationForm):

    def clean_username(self):
        return self.cleaned_data.get("username")
