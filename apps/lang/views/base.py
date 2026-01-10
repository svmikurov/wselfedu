"""Language discipline base views."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from dependency_injector.providers import Container
from dependency_injector.wiring import Provide, inject
from django.http.response import JsonResponse
from django.views import generic

from apps.core import views as core_views
from apps.lang import schemas, use_cases
from apps.lang.di import LanguageContainer
from di import MainContainer

from ..services import StudySettingsServiceABC

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

T = TypeVar('T')

CONTAINER: Container[LanguageContainer] = MainContainer.lang


class SettingsBaseView(
    generic.TemplateView,
    core_views.UserRequestMixin,
):
    """Settings base view."""

    _service: StudySettingsServiceABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        service: StudySettingsServiceABC = Provide[CONTAINER.settings_service],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject settings repository."""
        self._service = service
        return super().dispatch(request, *args, **kwargs)

    @property
    def service(self) -> StudySettingsServiceABC:
        """Get settings repository."""
        if not isinstance(self._service, StudySettingsServiceABC):
            raise AttributeError('Repository not initialized')
        return self._service


class BaseUseCaseView(
    generic.TemplateView,
    core_views.UserRequestMixin,
    Generic[T],
):
    """Base view provides user verification and UseCase."""

    _use_case: None | T = None

    @property
    def use_case(self) -> T:
        """Get presentation use case."""
        if self._use_case is None:
            raise AttributeError('UseCase not initialized')
        return self._use_case


class CaseBaseView(BaseUseCaseView[Presentation]):
    """Study case base view."""

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: Presentation = Provide[CONTAINER.web_presentation_use_case],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject presentation use case."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

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
