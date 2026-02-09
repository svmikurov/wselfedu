"""English translation study test exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views import generic

from apps.core.domain.exercise import CaseStatus
from apps.core.exceptions import info
from apps.core.handlers.types import WebAssignedTest, WebTest
from apps.core.views import auth, mixins
from di import MainContainer

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase


__all__ = [
    'TranslationTestView',
    'TranslationTestMentorshipView',
]

T = TypeVar('T')

CONTAINER = MainContainer.lang.view_container.exercise  # type: ignore

PARTIAL_TEMPLATES: dict[CaseStatus, str] = {
    CaseStatus.NEW_CASE: 'lang/exercise/test/_case.html',
    CaseStatus.EXPLAIN: 'lang/exercise/test/_explanation.html',
    CaseStatus.NO_CASE: 'lang/exercise/test/_no_cases.html',
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
        use_case: WebTest = Provide[CONTAINER.web_regular_test],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render translation study test case via partial template."""
        try:
            case = self.use_case.execute(self.user, request.POST.dict())
        except info.NoExerciseItemsException:
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
        use_case: WebAssignedTest = Provide[CONTAINER.web_detail_test],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render translation study test case via partial template."""
        try:
            case = self.use_case.execute(self.user, request.POST.dict(), pk=pk)
        except info.NoExerciseItemsException:
            template_name = PARTIAL_TEMPLATES[CaseStatus.NO_CASE]
            return HttpResponse(render_to_string(template_name))

        template_name = PARTIAL_TEMPLATES[case.status]
        context = case.data.model_dump()
        return HttpResponse(render_to_string(template_name, context))
