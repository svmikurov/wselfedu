"""CRUD of Term term DRF views."""

from typing import Type

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from contrib.views.general import (
    CheckLoginPermissionMixin,
    CheckUserOwnershipMixin,
    HandleNoPermissionMixin,
    PermissionProtectDeleteView,
)
from glossary.forms.term import TermForm
from glossary.models import Term


class TermCreateView(HandleNoPermissionMixin, LoginRequiredMixin, CreateView):
    """Create Term term view."""

    form_class = TermForm
    template_name = 'glossary/term_form.html'
    success_url = reverse_lazy('glossary:term_list')
    success_message = 'Термин добавлен'
    extra_context = {
        'title': 'Добавить термин в глоссарий',
    }

    def get_form(self, _: Form = None) -> FormHelper:
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = TermForm.apply_crispy_helper(form)
        return crispy_form

    def form_valid(self, form: Form) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class TermListView(CheckLoginPermissionMixin, ListView):
    """Term term list view."""

    model = Term
    template_name = 'glossary/term_list.html'
    context_object_name = 'terms'
    extra_context = {
        'title': 'Термины глоссария',
    }

    def get_queryset(self) -> QuerySet:
        """Get queryset to specific user."""
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .order_by('-created_at')
        )


class TermDetailView(CheckUserOwnershipMixin, DetailView):
    """Term term ditail View."""

    model = Term
    template_name = 'glossary/term_detail.html'
    context_object_name = 'term'


class TermUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update term view."""

    model = Term
    form_class = TermForm
    template_name = 'glossary/term_form.html'
    success_url = reverse_lazy('glossary:term_list')
    success_message = 'Термин изменен'
    context_object_name = 'term'
    extra_context = {
        'title': 'Изменить термин',
        'btn_name': 'Изменить',
    }

    def get_form(self, form_class: Type[Form] = None) -> FormHelper:
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = TermForm.apply_crispy_helper(form)
        return crispy_form


class TermDeleteView(PermissionProtectDeleteView):
    """Delete term view."""

    model = Term
    template_name = 'delete.html'
    success_url = reverse_lazy('glossary:term_list')
    success_message = 'Термин удален'
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }
