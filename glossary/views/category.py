"""Term term category views."""

from django.db.models import QuerySet
from django.forms import Form
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework.reverse import reverse_lazy

from contrib.views.general import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)
from glossary.forms.category import CategoryForm
from glossary.models import TermCategory


class CategoryCreateView(CheckLoginPermissionMixin, CreateView):
    """Create Term category view."""

    form_class = CategoryForm
    success_url = reverse_lazy('glossary:category_list')

    template_name = 'form.html'
    success_message = 'Категория добавлена'
    extra_context = {
        'title': 'Добавить категорию',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form: Form) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class CategoryListView(CheckLoginPermissionMixin, ListView):
    """Category list view."""

    model = TermCategory
    template_name = 'glossary/category_list.html'
    context_object_name = 'categories'
    extra_context = {
        'title': 'Категории терминов',
    }

    def get_queryset(self) -> QuerySet:
        """Get queryset to specific user."""
        queryset = super().get_queryset().filter(user=self.request.user.pk)
        return queryset


class CategoryUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Create category view."""

    model = TermCategory
    form_class = CategoryForm
    template_name = 'form.html'
    success_url = reverse_lazy('glossary:category_list')
    success_message = 'Категория слов изменена'
    extra_context = {
        'title': 'Изменить категорию',
        'btn_name': 'Изменить',
    }


class CategoryDeleteView(PermissionProtectDeleteView):
    """Delete category view."""

    model = TermCategory
    template_name = 'delete.html'
    success_url = reverse_lazy('glossary:category_list')
    success_message = 'Категория слов удалена'
    protected_redirect_url = reverse_lazy('glossary:category_list')
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        'title': 'Удаление категории',
        'btn_name': 'Удалить',
    }
