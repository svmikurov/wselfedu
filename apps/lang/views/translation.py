"""English translation CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django_filters import views as filter_views

from apps.core.generic.views import auth, htmx

from .. import filters, forms, models
from . import context, mixins

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse
    from django_filters.filterset import FilterSet


class EnglishTranslationCreateView(
    mixins.TranslationViewMixin,
    LoginRequiredMixin,
    generic.FormView,  # type: ignore[type-arg]
):
    """English translation create view."""

    form_class = forms.EnglishCreateForm
    template_name = 'lang/form.html'
    success_url = reverse_lazy('lang:translation_english_create')
    extra_context = context.ENGLISH_TRANSLATION['create']

    def form_valid(self, form: forms.EnglishCreateForm) -> HttpResponse:
        """Save translation."""
        self.repository.create(user=self.user, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationListView(
    mixins.TranslationViewMixin,
    LoginRequiredMixin,
    filter_views.FilterView,
):
    """English translation list view."""

    template_name = 'lang/translation_english_list.html'
    filterset_class = filters.TranslationFilter
    context_object_name = 'translations'
    paginate_by = 20
    extra_context = context.ENGLISH_TRANSLATION['list']

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get translation queryset."""
        return self.repository.get_translations(self.user)

    def get_filterset_kwargs(
        self, filterset_class: type[FilterSet]
    ) -> dict[str, Any]:
        """Add user to filter."""
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['user'] = self.user
        return kwargs


class EnglishTranslationUpdateView(
    mixins.TranslationViewMixin,
    auth.OwnershipRequiredMixin[models.EnglishTranslation],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """English translation update view."""

    model = models.EnglishTranslation
    form_class = forms.EnglishUpdateForm
    template_name = 'lang/form.html'
    success_url = reverse_lazy('lang:translation_english_list')
    extra_context = context.ENGLISH_TRANSLATION['update']

    def form_valid(self, form: forms.EnglishUpdateForm) -> HttpResponse:
        """Save translation."""
        instance = self.get_object()
        self.repository.update(self.user, instance, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationDeleteView(htmx.HtmxOwnerDeleteView):
    """English translation delete view."""

    model = models.EnglishTranslation
