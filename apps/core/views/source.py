"""Source views."""

from django.urls import reverse_lazy

from ..forms.source import SourceForm
from ..models import Source
from . import crud


class SourceListView(crud.BaseListView[Source]):
    """Source list view."""

    template_name = 'core/source/list.html'
    context_object_name = 'sources'
    paginate_by = 20
    model = Source


class SourceCreateView(crud.BaseCreateView):
    """Source create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('core:source_list')
    form_class = SourceForm


class SourceUpdateView(crud.BaseUpdateView[Source]):
    """Source update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('core:source_list')
    form_class = SourceForm
    model = Source


class SourceDeleteView(crud.HtmxOwnerDeleteView):
    """Source delete view."""

    model = Source
