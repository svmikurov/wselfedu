"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from dependency_injector.wiring import Provide, inject

from apps.core.assemblers.command import UserCommand, UserDataCommand
from apps.core.contracts import NullProtocol
from apps.core.contracts.response.web import OobResponseDTO
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
)
from apps.core.domains.exercise.presentation.dto import (
    PresentationMeta,
    PresentationTask,
)
from apps.core.domains.null import NullDTO
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.views.exercise import ExercisePerformView
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('TranslationPresentationView',)

_RequestData = RequestData

# =================================================
# Start exercise request handling types
# =================================================

type _StartResponseDTO = OobResponseDTO[
    ExerciseStatusEnum,
    PresentationTask,  # Adapted domain result data
    dict[str, Any],  # Extra context
]
type _StartHandler = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContext,  # Authentication required
    NullProtocol,  # No request data
    NullProtocol,  # No validated data
    UserCommand,  # Execute domain command by user
    # FIXME: Fix domain result type hint
    tuple[PresentationTask, PresentationMeta],  # Domain result
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
    # FIXME: Fix Any type hint
    Any,  # Domain result
    _ProcessResponseDTO,  # Response data for page template
]

# =================================================
# Exercise performing view
# =================================================

HANDLERS = MainContainer.lang.handlers  # type: ignore[unused-ignore]


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
            HANDLERS.process_regular_translation_presentation  # type: ignore[attr-defined]
        ],
        process_handler: _PrecessHandler = Provide[
            HANDLERS.process_regular_translation_presentation  # type: ignore[attr-defined]
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._start_handler = start_handler
        self._process_handler = process_handler
        return super().dispatch(request, *args, **kwargs)

    @override
    def _start(self, **kwargs: object) -> _StartResponseDTO:
        """Handel the GET request."""
        return self.start_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            # Request handler validates the request data.
            data=RequestData(data={'action': ExerciseProcessEnum.CREATE_CASE}),
        )

    @override
    def _process(self, **kwargs: object) -> _ProcessResponseDTO:
        """Handel the POST request."""
        return self.process_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            # Request handler validates the request data.
            data=RequestData(data=self.request.POST.dict()),
        )
