"""English translation study test exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views import generic

from apps.core.exceptions import info
from apps.core.views import auth, mixins
from apps.lang.schemas.test import CaseStatus
from apps.lang.use_cases.types import WebAssignedTest, WebTest
from di import MainContainer

if TYPE_CHECKING:
    from dependency_injector.providers import Container, Provider
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from apps.lang.di import ExercisesContainer, LanguageContainer

__all__ = [
    'TranslationTestView',
    'TranslationTestMentorshipView',
]

T = TypeVar('T')

CONTAINER: Container[LanguageContainer] = MainContainer.lang
EXERCISES: Provider[ExercisesContainer] = MainContainer.lang.exercises

PARTIAL_TEMPLATES: dict[CaseStatus, str] = {
    CaseStatus.NO_CASE: 'lang/exercise/test/_no_cases.html',
    CaseStatus.NEW: 'lang/exercise/test/_case.html',
    CaseStatus.EXPLANATION: 'lang/exercise/test/_explanation.html',
}

# REVIEW: Current implementation have duplicated dispatch method
#         with different use case injection.


class TranslationTestView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[WebTest],
    generic.TemplateView,
):
    """Translation study test exercise view."""

    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: WebTest = Provide[EXERCISES.web_test],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render translation study test case via partial template."""
        try:
            case = self.use_case.execute(self.user, request.POST.dict())
        except ValueError:
            template_name = PARTIAL_TEMPLATES[CaseStatus.NO_CASE]
            return HttpResponse(render_to_string(template_name))

        template_name = PARTIAL_TEMPLATES[case.status]
        context = case.data.model_dump()
        return HttpResponse(render_to_string(template_name, context))


class TranslationTestMentorshipView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[WebAssignedTest],
    generic.TemplateView,
):
    """Translation study test exercise view for mentorship."""

    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: WebAssignedTest = Provide[EXERCISES.web_test_mentorship],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render translation study test case via partial template."""
        try:
            case = self.use_case.execute(self.user, request.POST.dict(), pk=pk)
        except info.NoTranslationsAvailableException:
            template_name = PARTIAL_TEMPLATES[CaseStatus.NO_CASE]
            return HttpResponse(render_to_string(template_name))

        template_name = PARTIAL_TEMPLATES[case.status]
        context = case.data.model_dump()
        return HttpResponse(render_to_string(template_name, context))
