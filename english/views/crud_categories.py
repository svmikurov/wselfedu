from django.contrib.auth.mixins import LoginRequiredMixin
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
    ListView,
):
    model = CategoryModel
    context_object_name = 'categories'
    template_name = 'english/cat_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Список категорий',
    }

    def get_queryset(self):
        """Get categories added only by the current user."""
        queryset = super().get_queryset().filter(user=self.request.user.pk)
        return queryset


class CategoryCreateView(
    HandleNoPermissionMixin,
    AddMessageToFormSubmissionMixin,
    LoginRequiredMixin,
    CreateView,
):
    form_class = CategoryForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:categories_list')
    success_message = 'Категория добавлена'
    extra_context = {
        'title': 'Добавить категорию',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form):
        """Add current user to form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = CategoryModel
    form_class = CategoryForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:categories_list')
    success_message = 'Категория изменена'
    extra_context = {
        'title': 'Изменить категорию',
        'btn_name': 'Изменить',
    }


class CategoryDeleteView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    model = CategoryModel
    template_name = 'delete.html'
    success_url = reverse_lazy('english:categories_list')
    success_message = 'Категория удалена'
    extra_context = {
        'title': 'Удаление категории',
        'btn_name': 'Удалить',
    }
