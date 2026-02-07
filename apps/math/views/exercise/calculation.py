"""Calculation exercise view."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from apps.core.domain.exercise.enums import CaseStatus
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin
from apps.math.di.handler.types import (
    DetailCalculationWebHandler,
    RegularCalculationWebHandler,
)
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = [
    'DetailCalculationView',
    'RegularCalculationView',
]

CONTAINER = MainContainer.math.exercise_views

TEMPLATE_PATH = 'math/exercise/calculation/'
PARTIAL_TEMPLATES: dict[CaseStatus, str] = {
    CaseStatus.NEW_CASE: '_new_case.html',
    CaseStatus.EXPLAIN: '_explain_case.html',
    CaseStatus.NO_CASE: '_no_case.html',
}


class DetailCalculationView(
    UserLoginRequiredMixin,
    GetHandlerMixin[DetailCalculationWebHandler],
    TemplateView,
):
    """Detail calculation exercise view."""

    template_name = f'{TEMPLATE_PATH}index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: DetailCalculationWebHandler = Provide[
            CONTAINER.web_detail_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject calculation exercise request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponseBase:
        """Render the new exercise question or correct answer."""
        response_data = self.handler.execute(self.user, request.POST.dict())
        template_name = TEMPLATE_PATH + PARTIAL_TEMPLATES[response_data.status]
        context = self.get_context_data(**response_data.model_dump())
        return HttpResponse(render_to_string(template_name, context))


class RegularCalculationView(
    UserLoginRequiredMixin,
    GetHandlerMixin[RegularCalculationWebHandler],
    TemplateView,
):
    """Regular calculation exercise view."""

    template_name = f'{TEMPLATE_PATH}index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: RegularCalculationWebHandler = Provide[
            CONTAINER.web_regular_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject calculation exercise request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponseBase:
        """Render the new exercise question or correct answer."""
        response_data = self.handler.execute(self.user, request.POST.dict())
        template_name = TEMPLATE_PATH + PARTIAL_TEMPLATES[response_data.status]
        context = self.get_context_data(**response_data.model_dump())
        return HttpResponse(render_to_string(template_name, context))
