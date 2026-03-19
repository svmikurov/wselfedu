"""Base exercise view."""

from typing import Generic, TypeAlias, TypeVar, Union, override

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from apps.core.adapters.response.exercise.web.dto import (
    WebExerciseResponseDTO,
)
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.handlers.dto import (
    DetailRequestParams,
    QueryRequestParams,
    RequestContext,
    RequestData,
)
from apps.core.handlers.protocol import RequestHandlerProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetExerciseHandlersMixin

__all__ = (
    'ExercisePerformView',
    'QueryExercisePerformView',
    'DetailExercisePerformView',
)

QueryHandler: TypeAlias = RequestHandlerProtocol[
    QueryRequestParams[dict[str, str]],
    RequestContext,
    RequestData[dict[str, str]],
    WebExerciseResponseDTO,
]
DetailHandler: TypeAlias = RequestHandlerProtocol[
    DetailRequestParams,
    RequestContext,
    RequestData[dict[str, str]],
    WebExerciseResponseDTO,
]
Handler: TypeAlias = Union[QueryHandler, DetailHandler]

CreateHandler = TypeVar('CreateHandler', bound=Handler)
CheckHandler = TypeVar('CheckHandler', bound=Handler)

PARTIAL_TEMPLATES: dict[ExerciseStatusEnum, str] = {
    ExerciseStatusEnum.NEW_CASE: '_new_case.html',
    ExerciseStatusEnum.EXPLAIN: '_explain_case.html',
    ExerciseStatusEnum.NO_CASE: '_no_case.html',
}
ERROR_TEMPLATE = '_case_request_error.html'


class GetPartialExerciseTemplateMixin:
    """Mixin provides partial template for specific exercise status."""

    TEMPLATE_PATH: str

    def _get_partial_html(
        self,
        request: HttpRequest,
        schema: WebExerciseResponseDTO,
    ) -> str:
        """Get partial template html for exercise case."""
        try:
            template = PARTIAL_TEMPLATES[schema.exercise_status]
            context = schema.data.model_dump()
        except KeyError:
            template = ERROR_TEMPLATE
            context = {'error_message': _('Internal server error 500')}

        html = render_to_string(
            self.TEMPLATE_PATH + template, context, request
        )

        if request.headers.get('HX-Request'):
            return mark_safe(html + schema.oob_html)
        return html


class ExercisePerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[CreateHandler, CheckHandler],
    GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
    Generic[CreateHandler, CheckHandler],
):
    """Base exercise performing view."""

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial exercise page."""
        result = self._get_start_result(**kwargs)

        if request.headers.get('HX-Request') == 'true':
            # Renders new exercise case after explanation
            # via partial template.
            return HttpResponse(self._get_partial_html(request, result))

        else:
            # Renders initial exercise page.
            context: dict[str, str] = {
                'exercise_case_html': self._get_partial_html(request, result),
                **result.model_dump(),
            }
            return render(request, self.get_template_names(), context)

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render exercise loop."""
        # Query parameters contains exercise conditions.
        # Request body contains user's answer.
        result = self._get_check_result(**kwargs)
        return HttpResponse(self._get_partial_html(request, result))

    def _get_start_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        """Execute the start exercise and return result."""
        raise NotImplementedError()

    def _get_check_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        """Execute the exercise check and return result."""
        raise NotImplementedError()


class QueryExercisePerformView(
    ExercisePerformView[QueryHandler, QueryHandler]
):
    """Base query exercise perform view."""

    @override
    def _get_start_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        return self.start_handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    @override
    def _get_check_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        return self.check_handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )


class DetailExercisePerformView(
    ExercisePerformView[DetailHandler, DetailHandler]
):
    """Base detail exercise perform view."""

    @override
    def _get_start_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        return self.start_handler.execute(
            params=DetailRequestParams(pk=kwargs['pk']),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    @override
    def _get_check_result(self, **kwargs: object) -> WebExerciseResponseDTO:
        return self.check_handler.execute(
            params=DetailRequestParams(pk=int(kwargs['pk'])),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
