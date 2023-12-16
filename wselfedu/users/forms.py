from django.contrib.auth.forms import UserCreationForm

from wselfedu.users.models import UserModel


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ('username', 'password1', 'password2')


class UserUpdateForm(UserRegistrationForm):

    def clean_username(self):
        return self.cleaned_data.get("username")
