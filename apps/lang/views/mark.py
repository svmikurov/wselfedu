"""Language discipline mark CRUD views."""

from django.urls import reverse_lazy

from apps.core.views import crud

from ..forms import MarkForm
from ..models import Mark

__all__ = [
    'MarkListView',
    'MarkCreateView',
    'MarkUpdateView',
    'MarkDeleteView',
]


class MarkListView(crud.BaseListView[Mark]):
    """Mark list view."""

    template_name = 'lang/mark/index.html'
    context_object_name = 'marks'
    paginate_by = 15
    model = Mark


class MarkCreateView(crud.BaseCreateView):
    """Mark create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:mark_list')
    form_class = MarkForm


class MarkUpdateView(crud.BaseUpdateView[Mark]):
    """Mark update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:mark_list')
    form_class = MarkForm
    model = Mark


class MarkDeleteView(crud.HtmxOwnerDeleteView):
    """Mark delete view."""

    model = Mark
