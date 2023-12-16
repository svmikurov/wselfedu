from django.views.generic import UpdateView
from django.urls import reverse_lazy

from contrib_app.mixins import (
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
)
from users.forms import UserUpdateForm
from users.models import UserModel


class UserUpdateView(
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    """Updating a User Account."""

    model = UserModel
    form_class = UserUpdateForm
    extra_context = {
        'title': 'Обновление пользовательских данных',
        'btn_name': 'Обновить',
    }
    success_url = reverse_lazy('users:login')
    success_message = 'Вы обновили свои данные'
