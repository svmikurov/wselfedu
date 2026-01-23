"""English translation study test exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views import generic

from apps.core.views import auth, mixins
from apps.lang.schemas.test import CaseStatus
from apps.lang.use_cases import BaseUseCase
from di import MainContainer

if TYPE_CHECKING:
    from dependency_injector.providers import Container
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from apps.lang.di.container import LanguageContainer
    from apps.lang.schemas import test

    # Template types
    type Template = str
    type CaseTemplates = dict[CaseStatus, Template]

    # UseCase generic types
    type RequestData = dict[str, Any]
    type RequestDTO = test.TestRequestDTO
    type DomainResult = test.Case | test.Explanation
    type ResponseData = test.TestResponseData

type UseCase = BaseUseCase[RequestData, RequestDTO, DomainResult, ResponseData]

__all__ = [
    'TranslationTestView',
    'TranslationTestProgressView',
    'TranslationTestMentorshipView',
]

T = TypeVar('T')

CONTAINER: Container[LanguageContainer] = MainContainer.lang

PARTIAL_TEMPLATES: CaseTemplates = {
    CaseStatus.NO_CASE: 'lang/exercise/test/_no_cases.html',
    CaseStatus.NEW: 'lang/exercise/test/_case.html',
    CaseStatus.EXPLANATION: 'lang/exercise/test/_explanation.html',
}

# REVIEW: Current implementation have duplicated dispatch method
#         with different use case injection.


class _BaseTranslationTestView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[UseCase],
    generic.TemplateView,
):
    """Translation study test exercise base view."""

    template_name = 'lang/exercise/test/index.html'

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


class TranslationTestView(_BaseTranslationTestView):
    """Translation study test exercise view."""

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: UseCase = Provide[CONTAINER.web_test],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)


class TranslationTestProgressView(_BaseTranslationTestView):
    """Translation study test exercise view with progress tracking."""

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: UseCase = Provide[CONTAINER.web_test_progress],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)


class TranslationTestMentorshipView(
    auth.UserLoginRequiredMixin,
    mixins.GetUseCaseMixin[UseCase],
    generic.TemplateView,
):
    """Translation study test exercise view for mentorship."""

    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        use_case: UseCase = Provide[CONTAINER.web_test_mentorship],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject translation study test exercise UseCase."""
        self._use_case = use_case
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render translation study test case via partial template."""
        try:
            case = self.use_case.execute(
                self.user, request.POST.dict(), assignment_id=pk
            )
        except ValueError:
            template_name = PARTIAL_TEMPLATES[CaseStatus.NO_CASE]
            return HttpResponse(render_to_string(template_name))

        template_name = PARTIAL_TEMPLATES[case.status]
        context = case.data.model_dump()
        return HttpResponse(render_to_string(template_name, context))
