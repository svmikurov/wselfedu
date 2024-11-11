"""CRUD word sources views module."""

from typing import Type

from django.db import models
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from config.constants import (
    BTN_NAME,
    DELETE_TEMPLATE,
    DETAIL_SOURCE_TEMPLATE,
    FORM_TEMPLATE,
    PAGINATE_NUMBER,
    SOURCE_LIST_PATH,
    SOURCE_LIST_TEMPLATE,
    TITLE,
)
from contrib.views.general import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    PermissionProtectDeleteView,
)
from foreign.forms.source import SourceForm
from foreign.models import WordSource


class SourceCreateView(CheckLoginPermissionMixin, CreateView):
    """Create source view."""

    form_class = SourceForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов добавлен'
    extra_context = {
        TITLE: 'Добавить источник слов',
        BTN_NAME: 'Добавить',
    }

    def form_valid(self, form: Type[Form]) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class SourceUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update source view."""

    model = WordSource
    form_class = SourceForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов изменен'
    extra_context = {
        TITLE: 'Изменить источник слов',
        BTN_NAME: 'Изменить',
    }


class SourceDeleteView(PermissionProtectDeleteView):
    """Delete source view."""

    model = WordSource
    template_name = DELETE_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов удален'
    protected_redirect_url = reverse_lazy(SOURCE_LIST_PATH)
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )
    extra_context = {
        TITLE: 'Удаление источника слов',
        BTN_NAME: 'Удалить',
    }


class SourceListView(CheckLoginPermissionMixin, ListView):
    """List source view."""

    model = WordSource
    context_object_name = 'sources'
    template_name = SOURCE_LIST_TEMPLATE
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        TITLE: 'Источники',
    }

    def get_queryset(self) -> models.query.QuerySet:
        """Return the `QuerySet` to look up the object."""
        queryset = super().get_queryset().filter(user=self.request.user.id)
        return queryset


class SourceDetailView(CheckUserOwnershipMixin, DetailView):
    """Detail source view."""

    model = WordSource
    template_name = DETAIL_SOURCE_TEMPLATE
    context_object_name = 'source'
    extra_context = {
        TITLE: 'Обзор источника',
    }
