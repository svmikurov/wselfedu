"""English translation CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views import generic
from django_filters import views as filter_views

from apps.core import views as core_views
from apps.core.repositories.protocol import RepositoryProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin, GetRepositoryMixin
from di import MainContainer
from interfaces.protocols.request.general import RequestContextProtocol
from ports.contract.infra.handler import RequestHandlerProtocol
from ports.interfaces.protocols.web import (
    QueryRequestParamsProtocol,
    RequestDataProtocol,
)
from ports.interfaces.schemas.request.handler import (
    QueryRequestParams,
    RequestContext,
    RequestData,
)

from .. import filters, forms, models
from ..repositories import TranslationRepoABC

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http import HttpRequest, HttpResponse, HttpResponseBase

__all__ = [
    'EnglishTranslationIndexView',
    'EnglishTranslationListView',
    'EnglishTranslationCreateView',
    'EnglishTranslationUpdateView',
    'EnglishTranslationDeleteView',
]

ListHandler = RequestHandlerProtocol[
    QueryRequestParamsProtocol[dict[str, str]],
    RequestContextProtocol,
    RequestDataProtocol[dict[str, str]],
    QuerySet[models.EnglishTranslation],
]

HANDLERS = MainContainer.lang.handlers
REPOSITORIES = MainContainer.lang.repositories


class _TranslationViewMixin:
    """Provides repository injection and user property."""

    _repository: TranslationRepoABC | None = None

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


class EnglishTranslationListView(
    core_views.UserLoginRequiredMixin,
    GetHandlerMixin[ListHandler],
    filter_views.FilterView,
):
    """English translation list view."""

    template_name = 'lang/translation/list.html'
    context_object_name = 'translations'
    filterset_class = filters.TranslationFilter
    paginate_by = 20

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: ListHandler = Provide[HANDLERS.english_translation_list],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject repository before processing request."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get translation queryset."""
        return self.handler.execute(
            # Pass the request parameters query if need it.
            params=QueryRequestParams(query={}),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )


# HACK: Fix Any type hint
class EnglishTranslationCreateView(
    UserLoginRequiredMixin,
    GetRepositoryMixin[Any],
    generic.FormView,  # type: ignore[type-arg]
):
    """English translation create view."""

    template_name = 'lang/translation/create.html'
    success_url = reverse_lazy('lang:english_translation_create')
    form_class = forms.EnglishCreateForm

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: RepositoryProtocol[Any, Any] = Provide[
            REPOSITORIES.translation  # type: ignore
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject repository."""
        self._repository = repository
        return super().dispatch(request, *args, **kwargs)

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
