"""Calculation exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest
from django.views import View

from apps.core.views.exercise import (
    DetailExercisePerformMixin,
    QueryExercisePerformMixin,
)
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

type DetailHandler = Any
type QueryHandler = Any

__all__ = (
    'RegularPerformView',
    'CustomCalculationPerformView',
    'StudentCalculationPerformView',
)

HANDLERS = MainContainer.math.web_view


class RegularPerformView(QueryExercisePerformMixin, View):
    """Calculation exercise regular performing view."""

    TEMPLATE_PATH = 'math/exercise/calculation/perform/'
    template_name = 'math/exercise/calculation/perform/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: QueryHandler = Provide[
            HANDLERS.create_regular_calculation  # type: ignore[attr-defined]
        ],
        check_handler: QueryHandler = Provide[
            HANDLERS.check_regular_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = check_handler
        return super().dispatch(request, *args, **kwargs)


class CustomCalculationPerformView(DetailExercisePerformMixin, View):
    """User's saved calculation exercise performing view."""

    TEMPLATE_PATH = 'math/exercise/calculation/perform/'
    template_name = 'math/exercise/calculation/perform/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: DetailHandler = Provide[
            HANDLERS.start_custom_calculation  # type: ignore[attr-defined]
        ],
        check_handler: DetailHandler = Provide[
            HANDLERS.check_custom_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = check_handler
        return super().dispatch(request, *args, **kwargs)


class StudentCalculationPerformView(DetailExercisePerformMixin, View):
    """Student's assigned calculation exercise performing view."""

    TEMPLATE_PATH = 'math/exercise/calculation/perform/'
    template_name = 'math/exercise/calculation/perform/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: DetailHandler = Provide[
            HANDLERS.start_student_calculation  # type: ignore[attr-defined]
        ],
        check_handler: DetailHandler = Provide[
            HANDLERS.check_student_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = check_handler
        return super().dispatch(request, *args, **kwargs)


class MentorCalculationPerformView(DetailExercisePerformMixin, View):
    """Mentor's calculation exercise performing view."""

    TEMPLATE_PATH = 'math/exercise/calculation/perform/'
    template_name = 'math/exercise/calculation/perform/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: DetailHandler = Provide[
            HANDLERS.start_mentor_calculation  # type: ignore[attr-defined]
        ],
        check_handler: DetailHandler = Provide[
            HANDLERS.check_mentor_calculation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = check_handler
        return super().dispatch(request, *args, **kwargs)
