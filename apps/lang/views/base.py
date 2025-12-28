"""Language discipline base views."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views import View, generic
from django.views.generic.base import ContextMixin

from apps.core import views as core_views
from apps.lang import schemas, use_cases
from di import MainContainer

from .. import services

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from apps.lang import types
    from apps.lang.schemas import dto

    type Presentation = use_cases.BaseUseCase[
        dict[str, Any],
        schemas.PresentationRequest,
        dto.PresentationCase,
        types.TranslationWEB,
    ]


class SettingsBaseView(
    LoginRequiredMixin,
    generic.TemplateView,
    core_views.UserRequestMixin,
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
    ContextMixin,
    LoginRequiredMixin,
    core_views.UserRequestMixin,
    View,
):
    """Study case base view."""

    _use_case: Presentation | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: Presentation = Provide[
            MainContainer.lang.web_presentation_use_case
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject presentation use case."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    @property
    def use_case(self) -> Presentation:
        """Get presentation use case."""
        if not isinstance(self._use_case, use_cases.BaseUseCase):
            raise AttributeError('Service not initialized')
        return self._use_case

    def handle_no_permission(self) -> JsonResponse:  # type: ignore[override]
        """Render json response if user have no permissions."""
        return JsonResponse(
            data={
                'status': 'error',
                'message': 'authentication required',
                'authenticated': False,
                'login_url': self.get_login_url(),
                'next': self.request.get_full_path(),
            },
            status=HTTPStatus.UNAUTHORIZED,
        )
