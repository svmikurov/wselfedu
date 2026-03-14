"""Base regular exercise view."""

from __future__ import annotations

from typing import TypeAlias

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
    DetailParams,
    QueryParams,
    RequestContext,
    RequestData,
)
from apps.core.handlers.protocol import RequestHandlerProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetExerciseHandlersMixin

QueryHandler: TypeAlias = RequestHandlerProtocol[
    QueryParams,
    RequestContext,
    RequestData,
    WebExerciseResponseDTO,
]
DetailHandler: TypeAlias = RequestHandlerProtocol[
    DetailParams,
    RequestContext,
    RequestData,
    WebExerciseResponseDTO,
]

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


class BaseQueryPerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[QueryHandler, QueryHandler],
    GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
):
    """Base exercise performing view."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render initial exercise page."""
        result = self.start_handler.execute(
            params=QueryParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(query={}),
        )

        if request.headers.get('HX-Request') == 'true':
            # Renders new exercise case after explanation.
            return HttpResponse(self._get_partial_html(request, result))

        else:
            # Renders initial exercise page.
            context: dict[str, str] = {
                'exercise_case_html': self._get_partial_html(request, result),
                **result.model_dump(),
            }
            return render(request, self.get_template_names(), context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render exercise loop."""
        # Query parameters contains exercise conditions.
        # Request body contains user's answer.
        result = self.check_handler.execute(
            params=QueryParams(query=request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(query=request.POST.dict()),
        )
        return HttpResponse(self._get_partial_html(request, result))


class BaseDetailPerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[DetailHandler, DetailHandler],
    GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
):
    """Mixin provides request handling for detail exercise."""

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render initial exercise page."""
        result = self.start_handler.execute(
            params=DetailParams(pk=pk),
            context=RequestContext(user=self.user),
            data=RequestData(query={}),
        )

        if request.headers.get('HX-Request') == 'true':
            # Renders new exercise case after explanation.
            return HttpResponse(self._get_partial_html(request, result))

        else:
            # Renders initial exercise page.
            context: dict[str, str] = {
                'exercise_case_html': self._get_partial_html(request, result),
                **result.data.model_dump(),
                **result.context,
            }
            return render(request, self.get_template_names(), context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render exercise loop."""
        params = DetailParams(pk=pk)
        request_context = RequestContext(user=self.user)
        data = RequestData(query=request.POST.dict())

        result = self.check_handler.execute(params, request_context, data)
        return HttpResponse(self._get_partial_html(request, result))
