from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from contrib.mixins_views import (
    CheckAdminMixin,
    CheckObjectOwnershipMixin,
    FormMessageMixin,
    ObjectDeleteErrorMixin,
)
from users.forms import UserRegistrationForm, UserUpdateForm
from users.models import UserModel


class CreateUserView(FormMessageMixin, CreateView):
    """Create user view."""

    form_class = UserRegistrationForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь создан'
    extra_context = {
        'title': 'Регистрация пользователя',
        'btn_name': 'Зарегистрироваться',
    }


class UpdateUserView(CheckObjectOwnershipMixin, FormMessageMixin, UpdateView):
    """Update user view."""

    model = UserModel
    form_class = UserUpdateForm
    template_name = 'form.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь обновлен'
    extra_context = {
        'title': 'Обновление пользовательских данных',
        'btn_name': 'Обновить',
    }


class DeleteUserView(
    CheckObjectOwnershipMixin,
    FormMessageMixin,
    ObjectDeleteErrorMixin,
    DeleteView,
):
    """Delete user view."""

    template_name = 'delete.html'
    model = UserModel
    success_url = reverse_lazy('users:login')
    success_message = 'Пользователь удален'
    protected_redirect_url = reverse_lazy('home')
    protected_message = ('Невозможно удалить этот объект, так как он '
                         'используется в другом месте приложения')
    extra_context = {
        'title': 'Удаление пользователя',
        'btn_name': 'Удалить',
    }


class UsersListView(CheckAdminMixin, ListView):
    """User list view."""

    template_name = 'users/list.html'
    model = UserModel
    context_object_name = 'users'
