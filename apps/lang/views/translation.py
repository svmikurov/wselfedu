"""English translation CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.urls import reverse_lazy
from django.views import generic
from django_filters import views as filter_views

from apps.core import views as core_views
from di import MainContainer

from .. import filters, forms, models
from ..repositories.abc import TranslationRepoABC

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest, HttpResponse, HttpResponseBase
    from django_filters.filterset import FilterSet

__all__ = [
    'EnglishTranslationIndexView',
    'EnglishTranslationListView',
    'EnglishTranslationCreateView',
    'EnglishTranslationUpdateView',
    'EnglishTranslationDeleteView',
]

# REVIEW:


class _TranslationViewMixin:
    """Provides repository injection and user property."""

    _repository: TranslationRepoABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: TranslationRepoABC = Provide[
            MainContainer.lang.translation_repository
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject repository before processing request."""
        self._repository = repository
        return super().dispatch(request, *args, **kwargs)  # type: ignore[no-any-return, misc]

    @property
    def repository(self) -> TranslationRepoABC:
        """Get translation repository."""
        if not isinstance(self._repository, TranslationRepoABC):
            raise AttributeError('Repository not initialized')
        return self._repository


class EnglishTranslationIndexView(
    core_views.UserLoginRequiredMixin,
    generic.TemplateView,
):
    """English translation index view."""

    template_name = 'lang/translation/index.html'


# TODO: Fix database query count
class EnglishTranslationListView(
    core_views.UserLoginRequiredMixin,
    _TranslationViewMixin,
    filter_views.FilterView,
):
    """English translation list view."""

    template_name = 'lang/translation/list.html'
    context_object_name = 'translations'
    filterset_class = filters.TranslationFilter
    paginate_by = 20

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


class EnglishTranslationCreateView(
    core_views.UserLoginRequiredMixin,
    _TranslationViewMixin,
    generic.FormView,  # type: ignore[type-arg]
):
    """English translation create view."""

    template_name = 'lang/translation/create.html'
    success_url = reverse_lazy('lang:english_translation_create')
    form_class = forms.EnglishCreateForm

    def form_valid(self, form: forms.EnglishCreateForm) -> HttpResponse:
        """Save translation."""
        self.repository.create(user=self.user, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationUpdateView(
    _TranslationViewMixin,
    core_views.OwnershipRequiredMixin[models.EnglishTranslation],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """English translation update view."""

    template_name = 'lang/translation/update.html'
    success_url = reverse_lazy('lang:english_translation_list')
    form_class = forms.EnglishUpdateForm
    model = models.EnglishTranslation

    def form_valid(self, form: forms.EnglishUpdateForm) -> HttpResponse:
        """Save translation."""
        instance = self.get_object()
        self.repository.update(self.user, instance, **form.cleaned_data)
        return super().form_valid(form)


class EnglishTranslationDeleteView(core_views.HtmxOwnerDeleteView):
    """English translation delete view."""

    model = models.EnglishTranslation
