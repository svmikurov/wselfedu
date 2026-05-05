"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from apps.core.views.exercise import ExercisePerformView
from di import MainContainer

from ._types import HandlerT

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('TranslationPresentationView',)

HANDLERS = MainContainer.lang.handlers  # type: ignore[unused-ignore]


class TranslationPresentationView(ExercisePerformView[HandlerT]):
    """Regular translation test exercise performing view."""

    template_name = 'lang/exercise/presentation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: HandlerT = Provide[
            HANDLERS.regular_translation_presentation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)
