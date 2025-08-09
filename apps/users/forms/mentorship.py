"""Defines mentorship request form."""

from crispy_forms.helper import FormHelper  # type: ignore
from crispy_forms.layout import Field, Layout, Submit  # type: ignore
from django import forms


class SendMentorshipRequestForm(forms.Form):
    """Form to send request on mentorship."""

    mentor_username = forms.CharField(
        label='Введите "username" наставника',
    )

    def __init__(
        self,
        *args: object,
        **kwargs: object,
    ) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.attrs = {
            # HTMX uses current page url if hx-post = ''
            'hx-post': '',
            'hx-target': '#mentorship-requests',
        }
        self.helper.layout = Layout(
            Field('mentor_username'),
            Submit('submit', 'Отправить'),
        )
