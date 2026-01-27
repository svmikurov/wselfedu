"""English translation study test exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views import View

from apps.core.views import auth, mixins
from apps.lang.schemas.test import CaseStatus
from apps.lang.use_cases.types import WebTest
from di import MainContainer

if TYPE_CHECKING:
    from dependency_injector.providers import Container, Provider
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from apps.lang.di import LanguageContainer

__all__ = [
    'TranslationTestProgressView',
]

T = TypeVar('T')

CONTAINER: Container[LanguageContainer] = MainContainer.lang
EXERCISES: Provider[LanguageContainer] = MainContainer.lang.exercises

PARTIAL_TEMPLATES: dict[CaseStatus, str] = {
    CaseStatus.NO_CASE: 'lang/exercise/test/_no_cases.html',
    CaseStatus.NEW: 'lang/exercise/test/_case.html',
    CaseStatus.EXPLANATION: 'lang/exercise/test/_explanation.html',
}

# REVIEW: Relocate view definition?


class TranslationTestProgressView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[WebTest],
    View,
):
    """Translation study test exercise view with progress tracking."""

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: WebTest = Provide[EXERCISES.web_test_progress],  # type: ignore[attr-defined]
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
