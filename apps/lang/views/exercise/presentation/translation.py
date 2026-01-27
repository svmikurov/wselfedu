"""English translation study via presentation views."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from dependency_injector.providers import Provider
from dependency_injector.wiring import Provide, inject
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import generic

from apps.core.exceptions.info import NoTranslationsAvailableException
from apps.core.views import auth, mixins
from apps.lang import use_cases
from apps.lang.di import ExercisesContainer
from apps.lang.repositories.abc import StudySettingsRepositoryABC
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpResponseBase

    from apps.lang import schemas, types
    from apps.lang.schemas import dto

type Presentation = use_cases.UseCase[
    dict[str, Any],
    schemas.PresentationRequest,
    dto.PresentationCase,
    types.TranslationWEB,
]

__all__ = [
    'EnglishTranslationStudyView',
    'EnglishTranslationStudyCaseView',
]

EXERCISES: Provider[ExercisesContainer] = MainContainer.lang.exercises
REPOSITORIES: Provider[ExercisesContainer] = MainContainer.lang.repositories


class EnglishTranslationStudyView(
    auth.UserLoginRequiredMixin,
    mixins.GetRepositoryMixin[StudySettingsRepositoryABC],
    generic.TemplateView,
):
    """English translation study view.

    Renders the study page with study settings data for case request.
    The page requests a new study case as partial template to update.
    """

    template_name = 'lang/exercise/presentation/index.html'
    # HACK: Remove extra context
    extra_context = {
        'title': 'Изучение английских слов',
        'header': 'Изучение английских слов',
        'case_url': '/lang/translation/english/study/case/',
    }

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: StudySettingsRepositoryABC = Provide[
            REPOSITORIES.study_settings,  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject settings repository."""
        self._repository = repository
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add study settings to context."""
        context = super().get_context_data(**kwargs)
        context['study_setting'] = self.repository.fetch(self.user)
        return context


class EnglishTranslationStudyCaseView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[Presentation],
    generic.TemplateView,
):
    """English translation study case view."""

    _use_case: None | Presentation = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: Presentation = Provide[EXERCISES.web_presentation],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject presentation use case."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """If the case settings is valid, get and render the case."""
        try:
            case = self.use_case.execute(self.user, self.request.POST.dict())

        except NoTranslationsAvailableException:
            return self.handle_no_presentation_case()

        return self.render_partial(self.get_context_data(case=case))

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

    def render_partial(self, context: dict[str, Any]) -> HttpResponse:
        """Return response with template for partial page update."""
        template_dir = 'lang/exercise/presentation/'
        case = render_to_string(f'{template_dir}_case.html', context)
        mark = render_to_string(f'{template_dir}_mark_bar.html', context)
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
