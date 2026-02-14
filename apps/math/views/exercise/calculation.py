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
from apps.core.handlers.protocols import RegularRequestHandlerProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetExerciseHandlersMixin, GetHandlerMixin
from di import MainContainer

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

    type RequestData = dict[str, str]

type ChoiceHandler = Any
type GenerateHandler = Any
type CheckHandler = Any
type CreateHandler = Any

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

    def get_context_data(self, **kwargs: RequestData) -> RequestData:
        """Add data to context."""
        request_data = self.request.GET.dict()
        response_data = self.handler.execute(self.user, request_data)
        return super().get_context_data(**kwargs, **response_data.model_dump())


# -----------------------------------------------
# Calculation exercises
# -----------------------------------------------


class _BasePerformView(
    UserLoginRequiredMixin,
    GetExerciseHandlersMixin[CreateHandlerT, CheckHandlerT],
    TemplateResponseMixin,
    View,
    Generic[CreateHandlerT, CheckHandlerT],
):
    """Base exercise performing view."""

    template_name = 'math/exercise/calculation/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render initial exercise template."""
        schema = self.start_handler.execute(self.user, request.GET.dict())
        context: dict[str, str] = {
            'exercise_case_html': self._get_partial_html(request, schema),
            **schema.model_dump(),
        }
        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(self._get_partial_html(request, schema))
        else:
            return render(request, self.get_template_names(), context)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Render exercise template with stored exercise UUID."""
        schema = self.check_handler.execute(self.user, request.POST.dict())
        html = self._get_partial_html(request, schema)
        return HttpResponse(html)

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


class RegularPerformView(_BasePerformView[CreateHandler, CheckHandler]):
    """Calculation exercise regular performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        create_handler: CreateHandler = Provide[
            CONTAINER.create_regular_calculation  # type: ignore[attr-defined]
        ],
        check_handler: CheckHandler = Provide[
            CONTAINER.check_regular_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._create_handler = create_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)


class DetailPerformView(_BasePerformView[CreateHandler, CheckHandler]):
    """User's saved calculation exercise performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        create_handler: CreateHandler = Provide[
            CONTAINER.create_detail_calculation  # type: ignore[attr-defined]
        ],
        check_handler: CheckHandler = Provide[
            CONTAINER.check_detail_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._create_handler = create_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)


class AssignedPerformView(_BasePerformView[CreateHandler, CheckHandler]):
    """Assigned calculation exercise to user the performing view."""

    template_name = 'math/exercise/calculation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        create_handler: CreateHandler = Provide[
            CONTAINER.create_assigned_calculation  # type: ignore[attr-defined]
        ],
        check_handler: CheckHandler = Provide[
            CONTAINER.check_assigned_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._create_handler = create_handler
        self._check_handler = check_handler
        return super().dispatch(request, *args, **kwargs)
