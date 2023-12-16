from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from contrib_app.mixins import (
    CheckUserForOwnershipAccountMixin,
    HandleNoPermissionMixin,
)
from wselfedu.users.forms import UserRegistrationForm, UserUpdateForm
from wselfedu.users.models import UserModel


class UserRegistrationView(
    CreateView,
):
    form_class = UserRegistrationForm
    extra_context = {
        'title': 'Регистрация',
        'btn_name': 'Зарегистрироваться',
    }
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрировались'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class UserDetailView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    DetailView,
):
    model = UserModel
    extra_context = {
        'title': 'Личный кабинет',
    }


class UserUpdateView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    UpdateView,
):
    model = UserModel
    form_class = UserUpdateForm
    extra_context = {
        'title': 'Обновление пользовательских данных',
        'btn_name': 'Обновить',
    }
    success_message = 'Вы успешно обновили свои данные'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response


class UserDeleteView(
    HandleNoPermissionMixin,
    CheckUserForOwnershipAccountMixin,
    DeleteView,
):
    model = UserModel
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Удаление пользователя',
    }
    success_message = 'Пользователь удален'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
