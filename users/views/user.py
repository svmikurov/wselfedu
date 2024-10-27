"""User views."""

from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from config.constants import (
    BTN_NAME,
    DELETE_TEMPLATE,
    FORM_TEMPLATE,
    TITLE,
)
from contrib.views import (
    CheckAdminMixin,
    CheckObjectOwnershipMixin,
    FormMessageMixin,
    ObjectDeleteErrorMixin,
)
from users.forms import UserRegistrationForm, UserUpdateForm
from users.models import UserApp


class CreateUserView(FormMessageMixin, CreateView):
    """Create user view."""

    form_class = UserRegistrationForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь создан'
    extra_context = {
        TITLE: 'Регистрация пользователя',
        BTN_NAME: 'Зарегистрироваться',
    }


class UpdateUserView(CheckObjectOwnershipMixin, FormMessageMixin, UpdateView):
    """Update user view."""

    model = UserApp
    form_class = UserUpdateForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь обновлен'
    extra_context = {
        TITLE: 'Обновление пользовательских данных',
        BTN_NAME: 'Обновить',
    }


class DeleteUserView(
    CheckObjectOwnershipMixin,
    FormMessageMixin,
    ObjectDeleteErrorMixin,
    DeleteView,
):
    """Delete user view."""

    template_name = DELETE_TEMPLATE
    model = UserApp
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь удален'
    protected_redirect_url = reverse_lazy('home')
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        TITLE: 'Удаление пользователя',
        BTN_NAME: 'Удалить',
    }


class UsersListView(CheckAdminMixin, ListView):
    """User list view."""

    template_name = 'users/list.html'
    model = UserApp
    context_object_name = 'users'
