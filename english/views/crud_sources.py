"""CRUD word sources views module."""

from typing import Type

from django.db import models
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from contrib.mixins_views import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)
from english.forms.source import SourceForm
from english.models import SourceModel

SOURCE_LIST_PATH = 'english:source_list'

DELETE_SOURCE_TEMPLATE = 'delete.html'
DETAIL_SOURCE_TEMPLATE = 'english/source_detail.html'
SOURCE_FORM_TEMPLATE = 'form.html'
SOURCE_LIST_TEMPLATE = 'english/source_list.html'

PAGINATE_NUMBER = 20


class SourceCreateView(CheckLoginPermissionMixin, CreateView):
    """Create source view."""

    form_class = SourceForm
    template_name = SOURCE_FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов добавлен'
    extra_context = {
        'title': 'Добавить источник слов',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form: Type[Form]) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class SourceUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update source view."""

    model = SourceModel
    form_class = SourceForm
    template_name = SOURCE_FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов изменен'
    extra_context = {
        'title': 'Изменить источник слов',
        'btn_name': 'Изменить',
    }


class SourceDeleteView(PermissionProtectDeleteView):
    """Delete source view."""

    model = SourceModel
    template_name = DELETE_SOURCE_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов удален'
    protected_redirect_url = reverse_lazy(SOURCE_LIST_PATH)
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        'title': 'Удаление источника слов',
        'btn_name': 'Удалить',
    }


class SourceListView(CheckLoginPermissionMixin, ListView):
    """List source view."""

    model = SourceModel
    context_object_name = 'sources'
    template_name = SOURCE_LIST_TEMPLATE
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Источники',
    }

    def get_queryset(self) -> models.query.QuerySet:
        """Return the `QuerySet` to look up the object."""
        queryset = super().get_queryset().filter(user=self.request.user.id)
        return queryset


class SourceDetailView(CheckUserOwnershipMixin, DetailView):
    """Detail source view."""

    model = SourceModel
    template_name = DETAIL_SOURCE_TEMPLATE
    context_object_name = 'source'
    extra_context = {
        'title': 'Обзор источника',
    }
