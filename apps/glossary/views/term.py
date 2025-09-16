"""Term view."""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ...users.models import CustomUser
from ..models import Term


class TermCreateView(
    LoginRequiredMixin,
    CreateView,  # type: ignore[type-arg]
):
    """Create Term view."""

    model = Term
    fields = ['name', 'definition']
    success_url = reverse_lazy('glossary:term_create')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:  # type: ignore[type-arg]
        """Add user to save Term instance."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class TermDetailView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    DetailView,  # type: ignore[type-arg]
):
    """Detail Term view."""

    model = Term
    _object: Term | None = None

    def get_object(self, queryset: QuerySet[Term] | None = None) -> Term:
        """Cache the object after the first query."""
        if self._object is None:
            self._object = super().get_object(queryset)
        return self._object

    def test_func(self) -> bool:
        """Check that user is object owner."""
        return bool(self.request.user == self.get_object().user)


class TermUpdateView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    UpdateView,  # type: ignore[type-arg]
):
    """Update Term view."""

    model = Term
    fields = ['name', 'definition']
    success_url = reverse_lazy('glossary:term_list')
    _object: Term | None = None

    def get_object(self, queryset: QuerySet[Term] | None = None) -> Term:
        """Cache the object after the first query."""
        if self._object is None:
            self._object = super().get_object(queryset)
        return self._object

    def test_func(self) -> bool:
        """Check that user is object owner."""
        return bool(self.request.user == self.get_object().user)


class TermListView(
    LoginRequiredMixin,
    ListView,  # type: ignore[type-arg]
):
    """List Term view."""

    paginate_by = 10
    context_object_name = 'terms'

    def get_queryset(self) -> QuerySet[Term]:
        """Get Term list filtered by user."""
        if isinstance(self.request.user, CustomUser):
            return Term.objects.filter(user=self.request.user)
        return Term.objects.none()


class TermDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,  # type: ignore[type-arg]
):
    """Delete Term view."""

    model = Term
    success_url = reverse_lazy('glossary:term_list')
    _object: Term | None = None

    def get_object(self, queryset: QuerySet[Term] | None = None) -> Term:
        """Cache the object after the first query."""
        if self._object is None:
            self._object = super().get_object(queryset)
        return self._object

    def test_func(self) -> bool:
        """Check that user is object owner."""
        return bool(self.request.user == self.get_object().user)
