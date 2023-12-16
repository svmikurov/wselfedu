from django.views.generic import DeleteView
from django.urls import reverse_lazy

from contrib_app.mixins import (
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
)
from users.models import UserModel


class UserDeleteView(
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView
):
    """Deleting a user."""

    model = UserModel
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Удаление пользователя',
        'btn_name': 'Удалить',
    }
    success_message = 'Пользователь удален'
