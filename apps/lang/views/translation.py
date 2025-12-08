"""English word translation CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse_lazy
from django.views import generic

from .. import forms
from . import base

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpResponse

    from .. import models


class EnglishTranslationCreateView(
    base.TranslationView,
    generic.FormView,  # type: ignore[type-arg]
):
    """English translation create view."""

    form_class = forms.EnglishTranslationForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_english_create')

    def form_valid(self, form: forms.EnglishTranslationForm) -> HttpResponse:
        """Save translation."""
        self.repository.create_translation(self.user, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationListView(
    base.TranslationView,
    generic.ListView,  # type: ignore[type-arg]
):
    """English translation list view."""

    template_name = 'lang/translation_english_list.html'
    context_object_name = 'translations'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get translation queryset."""
        return self.repository.get_translations(self.user)
