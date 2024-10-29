"""CRUD of Glossary term DRF views."""

from typing import Type

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import Form
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from contrib.views import (
    CheckUserOwnershipMixin,
    HandleNoPermissionMixin,
    PermissionProtectDeleteView,
)
from glossary.forms.term import TermForm
from glossary.models import Glossary


class TermCreateView(HandleNoPermissionMixin, LoginRequiredMixin, CreateView):
    """Create Glossary term view."""

    form_class = TermForm
    template_name = 'glossary/term_form.html'
    extra_context = {
        'title': 'Добавить термин в глоссарий',
    }

    def get_form(self, _: Type[Form] = None) -> FormHelper:
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = TermForm.apply_crispy_helper(form)
        return crispy_form


class TermListView(ListView):
    """Glossary term list view."""

    model = Glossary
    template_name = 'glossary/term_list.html'
    context_object_name = 'terms'
    extra_context = {
        'title': 'Список терминов',
    }

    def get_queryset(self) -> QuerySet:
        """Get queryset to specific user."""
        return super().get_queryset().filter(user=self.request.user)


class TermDetailView(DetailView):
    """Glossary term ditail View."""

    model = Glossary
    template_name = 'glossary/term_detail.html'
    context_object_name = 'term'


class TermUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update term view."""

    model = Glossary
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

    model = Glossary
    template_name = 'delete.html'
    success_url = reverse_lazy('glossary:term_list')
    success_message = 'Слово удалено'
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }
