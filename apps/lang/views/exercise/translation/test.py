"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest

from apps.core.adapters.response.dto import ResponseDTO
from apps.core.domains.null import NullDTO
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.views.exercise import (
    ExercisePerformView,
    QueryHandler,
)
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('RegularTranslationTestPerformView',)

HANDLERS = MainContainer.lang.handlers


class RegularTranslationTestPerformView(
    ExercisePerformView[object, object, Any, Any]
):
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
        solve_handler: QueryHandler = Provide[
            HANDLERS.solve_regular_translation_test  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = solve_handler
        return super().dispatch(request, *args, **kwargs)

    @override
    def _start(self, **kwargs: object) -> ResponseDTO:
        return self.start_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            data=NullDTO(),
        )

    @override
    def _process(self, **kwargs: object) -> ResponseDTO:
        result = self.process_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
        return result
