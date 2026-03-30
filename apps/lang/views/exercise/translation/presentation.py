"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from dependency_injector.wiring import Provide, inject

from apps.core.adapters.response.dto import OobResponseDTO
from apps.core.assemblers.command import UserCommand, UserDataCommand
from apps.core.domains.exercise.enums import (
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.presentation.dto import (
    PresentationCase,
    PresentationMeta,
)
from apps.core.domains.null import NullDTO
from apps.core.domains.protocol import NullProtocol
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.views.exercise import ExercisePerformView
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('TranslationPresentationView',)

# =================================================
# Start exercise request handling types
# =================================================

type _StartResponseDTO = OobResponseDTO[
    ExerciseStatusEnum,
    PresentationCase,  # Adapted domain result data
    dict[str, Any],  # Extra context
]
type _StartHandler = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContext,  # Authentication required
    NullProtocol,  # No request data
    NullProtocol,  # No validated data
    UserCommand,  # Execute domain command by user
    tuple[PresentationCase, PresentationMeta],  # Domain result
    _StartResponseDTO,  # Response data for page template
]

# =================================================
# Process exercise request handling types
# =================================================

type _ProcessResponseDTO = OobResponseDTO[
    ExerciseStatusEnum,
    # FIXME: Fix Any type hint
    Any,  # Adapted domain result data
    dict[str, Any],  # Extra context
]
type _PrecessHandler = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContext,  # Authentication required
    RequestData[dict[str, Any]],  # Exercise performing request data
    # FIXME: Fix Any type hint
    Any,  # No validated data
    # FIXME: Fix Any type hint
    UserDataCommand[Any],  # Execute domain command by user
    Any,  # Domain result
    _ProcessResponseDTO,  # Response data for page template
]

# =================================================
# Exercise performing view
# =================================================

HANDLERS = MainContainer.lang.handlers


class TranslationPresentationView(
    ExercisePerformView[
        _StartHandler,
        _StartResponseDTO,
        _PrecessHandler,
        _ProcessResponseDTO,
    ],
):
    """Regular translation test exercise performing view."""

    TEMPLATE_PATH = 'lang/exercise/presentation/'
    template_name = 'lang/exercise/presentation/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: _StartHandler = Provide[
            HANDLERS.regular_translation_presentation  # type: ignore[attr-defined]
        ],
        process_handler: _PrecessHandler = Provide[
            HANDLERS.regular_translation_presentation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = process_handler
        return super().dispatch(request, *args, **kwargs)

    @override
    def _start(self, **kwargs: object) -> _StartResponseDTO:
        return self.start_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            data=NullDTO(),
        )

    @override
    def _process(self, **kwargs: object) -> _ProcessResponseDTO:
        return self.process_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
