"""Language discipline mark views."""

from __future__ import annotations

from django.urls import reverse_lazy

from apps.core import views as core_views

from ..forms import MarkForm
from ..models import Mark


class MarkListView(core_views.BaseListView[Mark]):
    """Mark list view."""

    template_name = 'lang/mark/index.html'
    context_object_name = 'marks'
    model = Mark
    paginate_by = 15


class MarkCreateView(core_views.BaseCreateView):
    """Mark create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:mark_list')
    form_class = MarkForm


class MarkUpdateView(core_views.BaseUpdateView[Mark]):
    """Mark update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:mark_list')
    model = Mark
    form_class = MarkForm


class MarkDeleteView(core_views.HtmxOwnerDeleteView):
    """Mark delete view."""

    model = Mark
