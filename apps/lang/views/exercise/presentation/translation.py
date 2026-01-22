"""English translation study views."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from dependency_injector.providers import Container
from dependency_injector.wiring import Provide, inject
from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from apps.core import views as core_views
from apps.core.exceptions.info import NoTranslationsAvailableException
from apps.lang import schemas, use_cases
from apps.lang.di import LanguageContainer
from di import MainContainer

from ....services import StudySettingsServiceABC

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


class BaseUseCaseView(
    core_views.UserLoginRequiredMixin,
    generic.TemplateView,
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


class SettingsBaseView(
    core_views.UserLoginRequiredMixin,
    generic.TemplateView,
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


class EnglishTranslationStudyView(SettingsBaseView):
    """English translation study view.

    Renders the study page with study settings data for case request.
    The page requests a new study case as partial template to update.
    """

    template_name = 'lang/presentation/index.html'
    # HACK: Remove extra context
    extra_context = {
        'title': 'Изучение английских слов',
        'header': 'Изучение английских слов',
        'case_url': '/lang/translation/english/study/case/',
    }

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add study settings to context."""
        context = super().get_context_data(**kwargs)
        context['study_setting'] = self.service.to_context(self.user)
        return context


class EnglishTranslationStudyCaseView(CaseBaseView):
    """English translation study case view."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """If the case settings is valid, get and render the case."""
        try:
            case = self.use_case.execute(self.user, self.request.POST.dict())

        except NoTranslationsAvailableException:
            messages.success(self.request, 'Нет переводов для изучения')
            return self.handle_no_presentation_case()

        return self.render_partial(self.get_context_data(case=case))

    def render_partial(self, context: dict[str, Any]) -> HttpResponse:
        """Return response with template for partial page update."""
        case = render_to_string('lang/presentation/_case.html', context)
        mark = render_to_string('lang/presentation/_mark_bar.html', context)
        combined_html = f'{case}\n{mark}'
        return HttpResponse(combined_html)

    def handle_no_presentation_case(self) -> JsonResponse:
        """Render json response if no presentation case."""
        return JsonResponse(
            data={
                'status': 'error',
                'message': 'No presentation case',
                'next': reverse('lang:settings'),
            },
            status=HTTPStatus.OK,
        )
