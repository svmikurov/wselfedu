"""English translation CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from apps.core.generic.views import auth

from .. import forms, models
from . import mixins

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse


class EnglishTranslationCreateView(
    mixins.TranslationViewMixin,
    LoginRequiredMixin,
    generic.FormView,  # type: ignore[type-arg]
):
    """English translation create view."""

    form_class = forms.EnglishTranslationCreateForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_english_create')

    def form_valid(
        self,
        form: forms.EnglishTranslationCreateForm,
    ) -> HttpResponse:
        """Save translation."""
        self.repository.create(self.user, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationListView(
    mixins.TranslationViewMixin,
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """English translation list view."""

    template_name = 'lang/translation_english_list.html'
    context_object_name = 'translations'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get translation queryset."""
        return self.repository.get_translations(self.user)


class EnglishTranslationUpdateView(
    mixins.TranslationViewMixin,
    auth.OwnershipRequiredMixin[models.EnglishTranslation],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """English translation update view."""

    model = models.EnglishTranslation
    form_class = forms.EnglishTranslationUpdateForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_english_list')

    def form_valid(
        self,
        form: forms.EnglishTranslationUpdateForm,
    ) -> HttpResponse:
        """Save translation."""
        instance = self.get_object()
        self.repository.update(self.user, instance, **form.cleaned_data)
        return super().form_valid(form)
