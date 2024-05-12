from django.views.generic import UpdateView, CreateView, DeleteView, \
    DetailView, ListView
from django.urls import reverse_lazy

from contrib_app.mixins import (
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
    RedirectForModelObjectDeleteErrorMixin, UserPassesTestAdminMixin,
    HandleNoPermissionMixin,
)
from users.forms import UserUpdateForm, UserRegistrationForm
from users.models import UserModel

LIST_PATH_NAME = 'users:login'
SUCCESS_DELETE_PATH = LIST_PATH_NAME
PROTECT_REDIRECT_URL = 'home'

SUCCESS_CREATE_USER_MSG = 'Пользователь создан'
SUCCESS_UPDATE_USER_MSG = 'Пользователь обновлен'
SUCCESS_DELETE_USER_MSG = 'Пользователь удален'
PROTECT_DELETE_USER_MSG = ('Невозможно удалить этот объект, так как он '
                           'используется в другом месте приложения')

DELETE_USER_TEMPLATE = 'delete.html'
DETAIL_USER_TEMPLATE = 'users/detail.html'
USER_FORM_TEMPLATE = 'form.html'
USER_LIST_TEMPLATE = 'users/list.html'


class CreateUserView(AddMessageToFormSubmissionMixin, CreateView):
    """Create user view."""

    form_class = UserRegistrationForm
    template_name = USER_FORM_TEMPLATE
    success_url = reverse_lazy(LIST_PATH_NAME)
    success_message = SUCCESS_CREATE_USER_MSG
    extra_context = {
        'title': 'Регистрация',
        'btn_name': 'Зарегистрироваться',
    }


class UpdateUserView(
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    """Update user view."""

    model = UserModel
    form_class = UserUpdateForm
    template_name = USER_FORM_TEMPLATE
    success_url = reverse_lazy(LIST_PATH_NAME)
    success_message = SUCCESS_UPDATE_USER_MSG
    extra_context = {
        'title': 'Обновление пользовательских данных',
        'btn_name': 'Обновить',
    }


class DeleteUserView(
    AccountOwnershipMixin,
    AddMessageToFormSubmissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    DeleteView,
):
    """Delete user view."""

    model = UserModel
    template_name = DELETE_USER_TEMPLATE
    success_url = reverse_lazy(SUCCESS_DELETE_PATH)
    success_message = SUCCESS_DELETE_USER_MSG
    protected_redirect_url = reverse_lazy(PROTECT_REDIRECT_URL)
    protected_message = PROTECT_DELETE_USER_MSG
    extra_context = {
        'title': 'Удаление пользователя',
        'btn_name': 'Удалить',
    }


class UsersListView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    ListView,
):
    """User list view."""

    model = UserModel
    template_name = USER_LIST_TEMPLATE
    context_object_name = 'users'
    extra_context = {
        'title': 'Список пользователей',
    }


class UserDetailView(AccountOwnershipMixin, DetailView):
    """User detail view."""

    model = UserModel
    template_name = DETAIL_USER_TEMPLATE
    extra_context = {
        'title': 'Личный кабинет',
    }
