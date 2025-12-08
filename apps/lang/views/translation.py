"""Word translation CRUD views."""

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
    """View to create English word translation to leaning."""

    form_class = forms.EnglishTranslationForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_english_create')

    def form_valid(self, form: forms.EnglishTranslationForm) -> HttpResponse:
        """Save word translation."""
        self.repository.create_translation(
            user=self.user,
            native=form.cleaned_data['native'],
            english=form.cleaned_data['english'],
        )
        return super().form_valid(form)


class EnglishTranslationListView(
    base.TranslationView,
    generic.ListView,  # type: ignore[type-arg]
):
    """View to render the English word translations list."""

    template_name = 'lang/translation_english_list.html'
    context_object_name = 'translations'
    paginate_by = 20

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get English word translations queryset."""
        return self.repository.get_translations(self.user)
