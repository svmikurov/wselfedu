from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from english.forms import CategoryForm
from english.models import CategoryModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

PAGINATE_NUMBER = 20


class CategoryListView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    ListView,
):
    model = CategoryModel
    context_object_name = 'categories'
    template_name = 'eng/cat_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Список категорий',
    }


class CategoryCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    CreateView,
):
    form_class = CategoryForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:cat_list')
    extra_context = {
        'title': 'Добавить категорию',
        'btn_name': 'Добавить',
    }

    success_message = 'Категория успешно добавлена'
    error_message = 'Ошибка в добавлении категории'


class CategoryUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = CategoryModel
    form_class = CategoryForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:cat_list')
    extra_context = {
        'title': 'Изменить категорию',
        'btn_name': 'Изменить',
    }

    success_message = 'Категория успешно изменена'
    error_message = 'Ошибка изменения категории'
    message_no_permission = 'Вы не можете этого делать'


class CategoryDeleteView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    model = CategoryModel
    template_name = 'delete.html'
    success_url = reverse_lazy('eng:cat_list')
    extra_context = {
        'title': 'Удаление категории',
        'btn_name': 'Удалить',
    }
