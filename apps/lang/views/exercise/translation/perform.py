"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest

from apps.core.views.exercise import (
    ExercisePerformView,
    QueryHandler,
)
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = (
    'RegularTranslationTestPerformView',
    'RegularTranslationPresentationPerformView',
)

HANDLERS = MainContainer.lang.web_handlers


# =================================================
# Translation presentation perform
# -------------------------------------------------


class RegularTranslationPresentationPerformView(ExercisePerformView):
    """Regular translation test exercise performing view."""

    TEMPLATE_PATH = 'lang/exercise/presentation/'
    template_name = 'lang/exercise/presentation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        create_handler: QueryHandler = Provide[
            HANDLERS.start_regular_translation_presentation  # type: ignore[attr-defined]
        ],
        # HACK: Fix the temporary handler stub
        solve_handler: QueryHandler = Provide[
            HANDLERS.start_regular_translation_presentation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._create_handler = create_handler
        self._solve_handler = solve_handler
        return super().dispatch(request, *args, **kwargs)


# =================================================
# Translation test perform
# -------------------------------------------------


class RegularTranslationTestPerformView(ExercisePerformView):
    """Regular translation test exercise performing view."""

    TEMPLATE_PATH = 'lang/exercise/test/'
    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: QueryHandler = Provide[
            HANDLERS.start_regular_translation_test  # type: ignore[attr-defined]
        ],
        # HACK: Fix the temporary handler stub
        solve_handler: QueryHandler = Provide[
            HANDLERS.start_regular_translation_test  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._solve_handler = solve_handler
        return super().dispatch(request, *args, **kwargs)
