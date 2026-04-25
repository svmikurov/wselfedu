"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from apps.core.views.exercise import ExercisePerformView
from apps.core.views.exercise.mixins import ExerciseLoopMixin
from di import MainContainer

from ._types import HandlerT, ResponseDtoT

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('RegularTranslationTestPerformView',)

HANDLERS = MainContainer.lang.handlers


class RegularTranslationTestPerformView(
    ExercisePerformView[HandlerT, ResponseDtoT],
    ExerciseLoopMixin,
):
    """Regular translation test exercise performing view."""

    TEMPLATE_PATH = 'lang/exercise/test/'
    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: HandlerT = Provide[
            HANDLERS.process_regular_translation_test  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)
