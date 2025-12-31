"""English translation study test exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string

from di import MainContainer

from ..schemas.test import CaseStatus
from ..use_cases import BaseUseCase
from ._data import ENGLISH_TRANSLATION
from .base import BaseUseCaseView

if TYPE_CHECKING:
    from dependency_injector.providers import Container
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from ..di.container import LanguageContainer
    from ..schemas import test

    # Template types
    type Template = str
    type CaseTemplates = dict[CaseStatus, Template]

    # UseCase generic types
    type RequestData = dict[str, Any]
    type RequestDTO = test.TestRequestDTO
    type DomainResult = test.Case | test.Explanation
    type ResponseData = test.TestResponseData


type UseCase = BaseUseCase[RequestData, RequestDTO, DomainResult, ResponseData]

CONTAINER: Container[LanguageContainer] = MainContainer.lang

PARTIAL_TEMPLATES: CaseTemplates = {
    CaseStatus.BAR: 'lang/test/_bar.html',
    CaseStatus.NEW: 'lang/test/_case.html',
    CaseStatus.EXPLANATION: 'lang/test/_explanation.html',
}


class _BaseTranslationTestView(BaseUseCaseView[UseCase]):
    """Translation study test exercise base view."""

    template_name = 'lang/test/index.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render translation study test case via partial template."""
        case = self.use_case.execute(self.user, request.POST.dict())
        template_name = PARTIAL_TEMPLATES[case.status]
        context = case.data.model_dump()
        return HttpResponse(render_to_string(template_name, context))


# TODO: Remove duplicate code
# Reason: Current implementation have duplicated dispatch method
#         with different use case injection.

# TODO: Remove duplicate code
# Reason: Current implementation have duplicated extra context.
# Question: Perhaps should move context to web adapter schema?


class TranslationTestView(_BaseTranslationTestView):
    """Translation study test exercise view."""

    extra_context = ENGLISH_TRANSLATION['translation_test']

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

    extra_context = ENGLISH_TRANSLATION['translation_test']

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


class TranslationTestMentorshipView(_BaseTranslationTestView):
    """Translation study test exercise view for mentorship."""

    extra_context = ENGLISH_TRANSLATION['translation_test']

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
