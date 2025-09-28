"""Language discipline label views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from apps.core.generic.views.auth import OwnershipRequiredMixin
from apps.users.models import CustomUser

from ..models import LangLabel


class LabelCreateView(
    LoginRequiredMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """View to create Language discipline label."""

    model = LangLabel
    fields = ['name']
    success_url = reverse_lazy('lang:label_create')
    template_name = 'lang/label_form.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:  # type: ignore[type-arg]
        """Add current user to form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class LabelUpdateView(
    OwnershipRequiredMixin[LangLabel],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """View to update Language discipline label."""

    model = LangLabel
    fields = ['name']
    template_name = 'lang/label_form.html'
    success_url = reverse_lazy('lang:label_list')


class LabelDeleteView(
    OwnershipRequiredMixin[LangLabel],
    generic.DeleteView,  # type: ignore[type-arg]
):
    """View to delete Language discipline label."""

    model = LangLabel
    success_url = reverse_lazy('lang:label_list')
    template_name = 'lang/label_confirm_delete.html'


class LabeDetailView(
    OwnershipRequiredMixin[LangLabel],
    generic.DetailView,  # type: ignore[type-arg]
):
    """View for detail Language discipline label."""

    model = LangLabel
    template_name = 'lang/label_detail.html'


class LabelListView(
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """View for list of Language discipline label."""

    paginate_by = 10
    context_object_name = 'labels'
    template_name = 'lang/label_list.html'

    def get_queryset(self) -> QuerySet[LangLabel]:
        """Get Label list filtered by user."""
        if isinstance(self.request.user, CustomUser):
            return LangLabel.objects.filter(user=self.request.user)
        return LangLabel.objects.none()
