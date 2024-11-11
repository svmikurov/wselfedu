"""CRUD word sources views module."""

from typing import Type

from django.db import models
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from config.constants import (
    PAGINATE_NUMBER,
)
from contrib.views.general import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)
from glossary.forms.source import SourceForm
from glossary.models import TermSource


class SourceCreateView(CheckLoginPermissionMixin, CreateView):
    """Create source view."""

    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('glossary:source_list')
    success_message = 'Источник терминов добавлен'
    extra_context = {
        'title': 'Добавить источник терминов',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form: Type[Form]) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class SourceUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update source view."""

    model = TermSource
    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('glossary:source_list')
    success_message = 'Источник терминов изменен'
    extra_context = {
        'title': 'Изменить источник терминов',
        'btn_name': 'Изменить',
    }


class SourceDeleteView(PermissionProtectDeleteView):
    """Delete source view."""

    model = TermSource
    template_name = 'delete.html'
    success_url = reverse_lazy('glossary:source_list')
    success_message = 'Источник терминов удален'
    protected_redirect_url = reverse_lazy('glossary:source_list')
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        'title': 'Удаление источника терминов',
        'btn_name': 'Удалить',
    }


class SourceListView(CheckLoginPermissionMixin, ListView):
    """List source view."""

    model = TermSource
    context_object_name = 'sources'
    template_name = 'glossary/source_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Источники терминов',
    }

    def get_queryset(self) -> models.query.QuerySet:
        """Return the `QuerySet` to look up the object."""
        queryset = super().get_queryset().filter(user=self.request.user.id)
        return queryset
