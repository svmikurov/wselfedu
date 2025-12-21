"""Language discipline base views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import edit

from apps.core import views as core_views
from di import MainContainer

from .. import adapters, services

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase


class SettingsBaseView(
    core_views.UserRequestMixin,
    LoginRequiredMixin,
    generic.TemplateView,
):
    """Settings base view."""

    _service: services.StudySettingsServiceABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        service: services.StudySettingsServiceABC = Provide[
            MainContainer.lang.settings_service,
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject settings repository."""
        self._service = service
        return super().dispatch(request, *args, **kwargs)

    @property
    def service(self) -> services.StudySettingsServiceABC:
        """Get settings repository."""
        if not isinstance(self._service, services.StudySettingsServiceABC):
            raise AttributeError('Repository not initialized')
        return self._service


class CaseBaseView(
    core_views.UserRequestMixin,
    LoginRequiredMixin,
    edit.BaseFormView,  # type: ignore[type-arg]
):
    """Study case base view."""

    _service: services.WordPresentationServiceABC | None = None
    _adapter: adapters.BaseTranslationAdapterWEB | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        service: services.WordPresentationServiceABC = Provide[
            MainContainer.lang.word_presentation_service,
        ],
        adapter: adapters.BaseTranslationAdapterWEB = Provide[
            MainContainer.lang.web_presentation,
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject dependencies."""
        self._service = service
        self._adapter = adapter
        if request.method != 'POST':
            return self.http_method_not_allowed(request)
        return super().dispatch(request, *args, **kwargs)

    @property
    def service(self) -> services.WordPresentationServiceABC:
        """Get case service."""
        if not isinstance(self._service, services.WordPresentationServiceABC):
            raise AttributeError('Service not initialized')
        return self._service

    @property
    def adapter(self) -> adapters.BaseTranslationAdapterWEB:
        """Get case service."""
        if not isinstance(self._adapter, adapters.BaseTranslationAdapterWEB):
            raise AttributeError('Adapter not initialized')
        return self._adapter
