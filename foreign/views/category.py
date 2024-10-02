"""CRUD word category views module."""

from typing import Type

from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from config.constants import (
    BTN_NAME,
    CATEGORIES,
    CATEGORY,
    CATEGORY_LIST_PATH,
    CATEGORY_LIST_TEMPLATE,
    DELETE_TEMPLATE,
    DETAIL_CATEGORY_TEMPLATE,
    FORM_TEMPLATE,
    PAGINATE_NUMBER,
    TITLE,
)
from contrib.mixins_views import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)
from foreign.forms import CategoryForm
from foreign.models import WordCategory


class CategoryCreateView(CheckLoginPermissionMixin, CreateView):
    """Create category view."""

    form_class = CategoryForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов добавлена'
    extra_context = {
        TITLE: 'Добавить категорию',
        BTN_NAME: 'Добавить',
    }

    def form_valid(self, form: Type[Form]) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CategoryUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Create category view."""

    model = WordCategory
    form_class = CategoryForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов изменена'
    extra_context = {
        TITLE: 'Изменить категорию',
        BTN_NAME: 'Изменить',
    }


class CategoryDeleteView(
    PermissionProtectDeleteView,
):
    """Delete category view."""

    model = WordCategory
    template_name = DELETE_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов удалена'
    protected_redirect_url = reverse_lazy(CATEGORY_LIST_PATH)
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        TITLE: 'Удаление категории',
        BTN_NAME: 'Удалить',
    }


class CategoryListView(CheckLoginPermissionMixin, ListView):
    """Category list view."""

    model = WordCategory
    template_name = CATEGORY_LIST_TEMPLATE
    context_object_name = CATEGORIES
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        TITLE: 'Категории',
    }

    def get_queryset(self) -> QuerySet:
        """Get queryset to specific user."""
        queryset = super().get_queryset().filter(user=self.request.user.pk)
        return queryset


class CategoryDetailView(CheckUserOwnershipMixin, DetailView):
    """Category detail view."""

    model = WordCategory
    template_name = DETAIL_CATEGORY_TEMPLATE
    context_object_name = CATEGORY
    extra_context = {
        TITLE: 'Обзор категории слов',
    }
