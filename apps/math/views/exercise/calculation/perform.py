"""Calculation exercise views."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import TemplateResponseMixin

from apps.core.adapter.response.exercise.web.dto import WebCase
from apps.core.domain.exercise.enums import ExerciseStatusEnum
from apps.core.handlers.dto import DetailParams, RequestContext, RequestData
from apps.core.handlers.protocol import (
    DetailRequestHandlerProtocol,
    RegularRequestHandlerProtocol,
)
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetExerciseHandlersMixin, GetHandlerMixin
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

type ChoiceHandler = Any
type GenerateHandler = Any
type CheckHandler = Any
type StartHandler = Any

CreateHandlerT = TypeVar(
    'CreateHandlerT', bound=RegularRequestHandlerProtocol[Any, Any]
)
CheckHandlerT = TypeVar(
    'CheckHandlerT', bound=RegularRequestHandlerProtocol[Any, Any]
)

__all__ = [
    'ExerciseChoiceView',
    'RegularPerformView',
    'DetailPerformView',
    'AssignedPerformView',
]

log = logging.getLogger(__name__)

CONTAINER = MainContainer.math.exercise_web_views

TEMPLATE_PATH = 'math/exercise/calculation/'
PARTIAL_TEMPLATES: dict[ExerciseStatusEnum, str] = {
    ExerciseStatusEnum.NEW_CASE: '_new_case.html',
    ExerciseStatusEnum.EXPLAIN: '_explain_case.html',
    ExerciseStatusEnum.NO_CASE: '_no_case.html',
}
ERROR_TEMPLATE = '_case_request_error.html'

# -----------------------------------------------
# Calculation conditions
# -----------------------------------------------


class ExerciseChoiceView(
    UserLoginRequiredMixin,
    GetHandlerMixin[ChoiceHandler],
    TemplateView,
):
    """Select calculation exercise.

    Renders:
      - form for the exercise conditions
      - table of exercises saved by the user (not yet implemented)
      - table of exercises assigned to the user (not yet implemented)
    """

    template_name = 'math/exercise/calculation/conditions.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: ChoiceHandler = Provide[
            CONTAINER.calculation_exercise_choice  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, str]) -> dict[str, str]:
        """Add data to context."""
        request_data = self.request.GET.dict()
        response_data = self.handler.execute(self.user, request_data)
        return super().get_context_data(**kwargs, **response_data.model_dump())


# -----------------------------------------------
# Calculation exercises
# -----------------------------------------------


class GetPartialExerciseTemplateMixin:
    """Mixin provides partial template for specific exercise status."""

    @staticmethod
    def _get_partial_html(request: HttpRequest, schema: WebCase) -> str:
        """Get partial template html for exercise case."""
        try:
            template = PARTIAL_TEMPLATES[schema.exercise_status]
            context = schema.data.model_dump()
        except KeyError:
            template = ERROR_TEMPLATE
            context = {'error_message': _('Internal server error 500')}
        return render_to_string(TEMPLATE_PATH + template, context, request)


class _BasePerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[CreateHandlerT, CheckHandlerT],
    GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
    Generic[CreateHandlerT, CheckHandlerT],
):
    """Base exercise performing view."""

    template_name = 'math/exercise/calculation/index.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render exercise template with stored exercise UUID."""
        result = self.check_handler.execute(self.user, request.POST.dict())
        html = self._get_partial_html(request, result)
        return HttpResponse(html)


class RegularPerformView(_BasePerformView[StartHandler, CheckHandler]):
    """Calculation exercise regular performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: StartHandler = Provide[
            CONTAINER.create_regular_calculation  # type: ignore[attr-defined]
        ],
        check_handler: CheckHandler = Provide[
            CONTAINER.check_regular_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render initial exercise template."""
        result = self.start_handler.execute(self.user, request.GET.dict())
        context: dict[str, str] = {
            'exercise_case_html': self._get_partial_html(request, result),
            **result.model_dump(),
        }
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(self._get_partial_html(request, result))
        else:
            return render(request, self.get_template_names(), context)


class DetailPerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[
        DetailRequestHandlerProtocol[WebCase],
        DetailRequestHandlerProtocol[WebCase],
    ],
    GetPartialExerciseTemplateMixin,
    TemplateResponseMixin,
    View,
):
    """User's saved calculation exercise performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: DetailRequestHandlerProtocol[WebCase] = Provide[
            CONTAINER.start_detail_calculation  # type: ignore[attr-defined]
        ],
        check_handler: DetailRequestHandlerProtocol[WebCase] = Provide[
            CONTAINER.check_detail_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render initial exercise template."""
        params = DetailParams(pk=pk)
        meta = RequestContext(user=self.user)
        data = RequestData(query=request.GET.dict())
        result = self.start_handler.execute(params, meta, data)

        context: dict[str, str] = {
            'exercise_case_html': self._get_partial_html(request, result),
            **result.data.model_dump(),
        }
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(self._get_partial_html(request, result))
        else:
            return render(request, self.get_template_names(), context)

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        """Render exercise template with stored exercise UUID."""
        params = DetailParams(pk=pk)
        request_context = RequestContext(user=self.user)
        data = RequestData(query=request.POST.dict())
        result = self.check_handler.execute(params, request_context, data)

        html = self._get_partial_html(request, result)
        return HttpResponse(html)


class AssignedPerformView(_BasePerformView[StartHandler, CheckHandler]):
    """Assigned calculation exercise to user the performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        create_handler: StartHandler = Provide[
            CONTAINER.create_assigned_calculation  # type: ignore[attr-defined]
        ],
        check_handler: CheckHandler = Provide[
            CONTAINER.check_assigned_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = create_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)
