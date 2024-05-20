from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from english.forms import CategoryForm
from english.models import CategoryModel
from contrib.mixins_views import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)

CREATE_CATEGORY_PATH = 'english:categories_create'
CATEGORY_LIST_PATH = 'english:category_list'

DELETE_CATEGORY_TEMPLATE = 'delete.html'
DETAIL_CATEGORY_TEMPLATE = 'english/category_detail.html'
CATEGORY_FORM_TEMPLATE = 'form.html'
CATEGORY_LIST_TEMPLATE = 'english/category_list.html'

PAGINATE_NUMBER = 20


class CategoryCreateView(CheckLoginPermissionMixin, CreateView):
    """Create category view."""

    form_class = CategoryForm
    template_name = CATEGORY_FORM_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов добавлена'
    extra_context = {
        'title': 'Добавить категорию',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form):
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CategoryUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Create category view."""

    model = CategoryModel
    form_class = CategoryForm
    template_name = CATEGORY_FORM_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов изменена'
    extra_context = {
        'title': 'Изменить категорию',
        'btn_name': 'Изменить',
    }


class CategoryDeleteView(
    PermissionProtectDeleteView,
):
    """Delete category view."""

    model = CategoryModel
    template_name = DELETE_CATEGORY_TEMPLATE
    success_url = reverse_lazy(CATEGORY_LIST_PATH)
    success_message = 'Категория слов удалена'
    protected_redirect_url = reverse_lazy(CATEGORY_LIST_PATH)
    protected_message = ('Невозможно удалить этот объект, так как он '
                         'используется в другом месте приложения')
    extra_context = {
        'title': 'Удаление категории',
        'btn_name': 'Удалить',
    }


class CategoryListView(CheckLoginPermissionMixin, ListView):
    """Category list view."""

    model = CategoryModel
    template_name = CATEGORY_LIST_TEMPLATE
    context_object_name = 'categories'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Категории',
    }

    def get_queryset(self):
        """Get queryset to specific user."""
        queryset = super().get_queryset(
        ).filter(
            user=self.request.user.pk
        )
        return queryset


class CategoryDetailView(CheckUserOwnershipMixin, DetailView):
    """Category detail view."""

    model = CategoryModel
    template_name = DETAIL_CATEGORY_TEMPLATE
    context_object_name = 'category'
    extra_context = {
        'title': 'Обзор категории слов'
    }
