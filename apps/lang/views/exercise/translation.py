"""English discipline translation exercise views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from apps.core.views.exercise import ExercisePerformView
from di import MainContainer

from ._types import PresentationHandlerT, TestHandlerT

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('TranslationPresentationView',)

HANDLERS = MainContainer.lang.handlers  # type: ignore[unused-ignore]


class TranslationPresentationView(ExercisePerformView[PresentationHandlerT]):
    """Regular translation test exercise performing view."""

    template_name = 'lang/exercise/presentation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: PresentationHandlerT = Provide[
            HANDLERS.regular_translation_presentation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)


class RegularTranslationTestPerformView(ExercisePerformView[TestHandlerT]):
    """Regular translation test exercise performing view."""

    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: TestHandlerT = Provide[
            HANDLERS.regular_translation_test  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)
