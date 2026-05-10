"""Calculation exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest
from django.views.generic import TemplateView

from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin
from di import MainContainer
from ports.interfaces.schemas.request.handler import (
    QueryRequestParams,
    RequestContext,
    RequestData,
)

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

type QueryHandler = Any

__all__ = ('ExerciseChoiceView',)

HANDLERS = MainContainer.math.web_view


class ExerciseChoiceView(
    UserLoginRequiredMixin,
    GetHandlerMixin[QueryHandler],
    TemplateView,
):
    """Select calculation exercise."""

    template_name = 'math/exercise/calculation/regular/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: QueryHandler = Provide[HANDLERS.calculation_exercise_choice],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, str]) -> dict[str, str]:
        """Add data to context."""
        response_data = self.handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )
        return super().get_context_data(**kwargs, **response_data.model_dump())
