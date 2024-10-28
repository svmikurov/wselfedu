"""CRUD of Glossary term DRF views."""

from typing import Type

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import Form
from django.views.generic import CreateView, DetailView, ListView

from contrib.views import HandleNoPermissionMixin
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


class TermDitailView(DetailView):
    """Glossary term ditail View."""

    model = Glossary
    template_name = 'glossary/term_detail.html'
    context_object_name = 'term'
