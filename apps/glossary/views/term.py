"""Term view."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from apps.core.generic.views.auth import OwnershipRequiredMixin
from apps.users.models import CustomUser

from ..models import Term


class TermCreateView(
    LoginRequiredMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Create Term view."""

    model = Term
    fields = ['name', 'definition']
    success_url = reverse_lazy('glossary:term_create')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:  # type: ignore[type-arg]
        """Add user to save Term instance."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TermUpdateView(
    OwnershipRequiredMixin[Term],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """Update Term view."""

    model = Term
    fields = ['name', 'definition']
    success_url = reverse_lazy('glossary:term_list')


class TermDeleteView(
    OwnershipRequiredMixin[Term],
    generic.DeleteView,  # type: ignore[type-arg]
):
    """Delete Term view."""

    model = Term
    success_url = reverse_lazy('glossary:term_list')


class TermDetailView(
    OwnershipRequiredMixin[Term],
    generic.DetailView,  # type: ignore[type-arg]
):
    """Detail Term view."""

    model = Term


class TermListView(
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """List Term view."""

    paginate_by = 10
    context_object_name = 'terms'

    def get_queryset(self) -> QuerySet[Term]:
        """Get Term list filtered by user."""
        if isinstance(self.request.user, CustomUser):
            return Term.objects.filter(user=self.request.user)
        return Term.objects.none()
