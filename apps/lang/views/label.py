"""Language discipline mark views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from apps.core.generic.views.auth import OwnershipRequiredMixin
from apps.users.models import CustomUser

from ..models import LangMark


class MarkCreateView(
    LoginRequiredMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """View to create Language discipline mark."""

    model = LangMark
    fields = ['name']
    success_url = reverse_lazy('lang:mark_create')
    template_name = 'lang/mark_form.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:  # type: ignore[type-arg]
        """Add current user to form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class MarkUpdateView(
    OwnershipRequiredMixin[LangMark],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """View to update Language discipline mark."""

    model = LangMark
    fields = ['name']
    template_name = 'lang/mark_form.html'
    success_url = reverse_lazy('lang:mark_list')


class MarkDeleteView(
    OwnershipRequiredMixin[LangMark],
    generic.DeleteView,  # type: ignore[type-arg]
):
    """View to delete Language discipline mark."""

    model = LangMark
    success_url = reverse_lazy('lang:mark_list')
    template_name = 'lang/mark_confirm_delete.html'


class MarkDetailView(
    OwnershipRequiredMixin[LangMark],
    generic.DetailView,  # type: ignore[type-arg]
):
    """View for detail Language discipline mark."""

    model = LangMark
    template_name = 'lang/mark_detail.html'


class LabelListView(
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """View for list of Language discipline mark."""

    paginate_by = 10
    context_object_name = 'marks'
    template_name = 'lang/mark_list.html'

    def get_queryset(self) -> QuerySet[LangMark]:
        """Get Label list filtered by user."""
        if isinstance(self.request.user, CustomUser):
            return LangMark.objects.filter(user=self.request.user)
        return LangMark.objects.none()
