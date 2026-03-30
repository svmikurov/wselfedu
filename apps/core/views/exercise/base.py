"""Base exercise view."""

import logging
from typing import Any, Generic, TypeAlias, TypeVar, Union, override

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from apps.core.adapters.response.dto import OobResponseDTO
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.handlers.dto import (
    DetailRequestParams,
    QueryRequestParams,
    RequestContext,
    RequestData,
)
from apps.core.handlers.protocol import RequestHandlerProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import (
    ProcessExerciseHandlerMixin,
    StartExerciseHandlerMixin,
)

__all__ = (
    'ExercisePerformView',
    'DeprecatedExercisePerformView',
    'QueryExercisePerformView',
    'DetailExercisePerformView',
)

log = logging.getLogger(__name__)

ResponseDTOtype: TypeAlias = OobResponseDTO[object, object, object]

QueryHandler: TypeAlias = RequestHandlerProtocol[
    QueryRequestParams[dict[str, str]],
    RequestContext,
    RequestData[dict[str, str]],
    ResponseDTOtype,
]
DetailHandler: TypeAlias = RequestHandlerProtocol[
    DetailRequestParams,
    RequestContext,
    RequestData[dict[str, str]],
    ResponseDTOtype,
]

Handler: TypeAlias = Union[QueryHandler, DetailHandler]

StartHandler = TypeVar('StartHandler')
ProcessHandler = TypeVar('ProcessHandler')
ResponseDTO = TypeVar('ResponseDTO')
StartResponseDTO = TypeVar('StartResponseDTO')
ProcessResponseDTO = TypeVar('ProcessResponseDTO')

PARTIAL_TEMPLATES: dict[ResponseStatusEnum, str] = {
    ResponseStatusEnum.NEW_CASE: '_new_case.html',
    ResponseStatusEnum.EXPLAIN_CASE: '_explain_case.html',
    ResponseStatusEnum.NO_CASE: '_no_case.html',
}
ERROR_TEMPLATE = '_case_request_error.html'


# =================================================
# Exercise view mixins
# =================================================


class _GetPartialExerciseTemplateMixin:
    """Mixin provides partial template for specific exercise status."""

    TEMPLATE_PATH: str

    def _get_partial_html(
        self,
        request: HttpRequest,
        schema: ResponseDTOtype,
    ) -> str:
        """Get partial template html for exercise case."""
        try:
            template = PARTIAL_TEMPLATES[schema.status]  # type: ignore
            context = schema.context.model_dump()  # type: ignore
        except KeyError as exc:
            log.exception(f'Get template key error: {exc}')
            template = ERROR_TEMPLATE
            context = {'error_message': _('Internal server error 500')}

        html = render_to_string(self.TEMPLATE_PATH + template, context)

        if request.headers.get('HX-Request'):
            return mark_safe(html + schema.oob_html)

        return html


# =================================================
# Exercise views
# =================================================

# REVIEW: Exercise view inherit


class StartExerciseView(
    UserLoginRequiredMixin,
    StartExerciseHandlerMixin[StartHandler],
    _GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
    Generic[StartHandler, StartResponseDTO],
):
    """Start exercise performing view."""

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial exercise page."""
        result = self._start(**kwargs)

        if request.headers.get('HX-Request') == 'true':
            # Renders new exercise case after explanation
            # via partial template.
            return HttpResponse(self._get_partial_html(request, result))  # type: ignore

        else:
            # Renders initial exercise page.
            context: dict[str, str] = {
                'exercise_case_html': self._get_partial_html(request, result),  # type: ignore
                **result.model_dump(),  # type: ignore
            }

            return render(request, self.get_template_names(), context)

    def _start(self, **kwargs: object) -> StartResponseDTO:
        """Create and provide exercise case."""
        raise NotImplementedError()


class ProcessExerciseView(
    UserLoginRequiredMixin,
    ProcessExerciseHandlerMixin[ProcessHandler],
    _GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
    Generic[ProcessHandler, ProcessResponseDTO],
):
    """Process exercise performing view."""

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render the process result of exercise performing."""
        # Query parameters contains exercise conditions.
        # Request body contains user's answer.
        result = self._process(**kwargs)
        return HttpResponse(self._get_partial_html(request, result))  # type: ignore

    def _process(self, **kwargs: object) -> ProcessResponseDTO:
        """Process exercise performing."""
        raise NotImplementedError()


class ExercisePerformView(
    StartExerciseView[StartHandler, StartResponseDTO],
    ProcessExerciseView[ProcessHandler, ProcessResponseDTO],
    Generic[
        StartHandler, StartResponseDTO, ProcessHandler, ProcessResponseDTO
    ],
):
    """Base exercise performing view."""


# =================================================
# Exercise request types
# =================================================


class DeprecatedExercisePerformView(
    ExercisePerformView[QueryHandler, QueryHandler, Any, Any]
):
    """Exercise perform view."""

    @override
    def _start(self, **kwargs: object) -> ResponseDTOtype:  # type: ignore
        return self.start_handler.execute(
            params=QueryRequestParams(query={}),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    @override
    def _process(self, **kwargs: object) -> ResponseDTOtype:
        return self.process_handler.execute(  # type: ignore
            params=QueryRequestParams(query={}),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )


class QueryExercisePerformView(
    ExercisePerformView[QueryHandler, QueryHandler, Any, Any]
):
    """Base query exercise perform view."""

    @override
    def _start(self, **kwargs: object) -> ResponseDTOtype:  # type: ignore
        return self.start_handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    @override
    def _process(self, **kwargs: object) -> ResponseDTOtype:
        return self.process_handler.execute(  # type: ignore
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )


class DetailExercisePerformView(
    ExercisePerformView[DetailHandler, DetailHandler, Any, Any]
):
    """Base detail exercise perform view."""

    @override
    def _start(self, **kwargs: object) -> ResponseDTOtype:  # type: ignore
        return self.start_handler.execute(
            params=DetailRequestParams(pk=kwargs['pk']),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    @override
    def _process(self, **kwargs: object) -> ResponseDTOtype:
        return self.process_handler.execute(  # type: ignore
            params=DetailRequestParams(pk=int(kwargs['pk'])),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
