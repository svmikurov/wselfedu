"""English translation perform views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from dependency_injector.wiring import Provide, inject
from django.http.request import HttpRequest

# from apps.core.validators.request.exercise
from apps.core.adapters.response.dto import OobResponseDTO
from apps.core.assemblers.protocol import UserCommandProtocol
from apps.core.contracts import NullProtocol
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.test.dto import (
    OptionMetaDTO,
    TestExerciseMeta,
)
from apps.core.domains.null import NullDTO
from apps.core.handlers.dto import RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.handlers.protocol import (
    RequestContextProtocol,
    RequestDataProtocol,
)
from apps.core.views.exercise import (
    ExercisePerformView,
)
from di import MainContainer

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponseBase

__all__ = ('RegularTranslationTestPerformView',)

# =================================================
# Start exercise request handling types
# =================================================

type _StartResponseDTO = OobResponseDTO[
    ExerciseStatusEnum,  # Domain status enumeration
    TestExerciseMeta[OptionMetaDTO],  # Template exercise data
    dict[str, Any],  # Extra context for template
]
type _StartHandler = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContextProtocol,  # Authentication required
    NullProtocol,  # No request data
    NullProtocol,  # No validated data
    UserCommandProtocol,  # Execute use case by user command
    tuple[
        TestExerciseMeta[OptionMetaDTO],
        TestExerciseMeta[OptionMetaDTO],
    ],  # Domain result
    _StartResponseDTO,  # Response data for template
]

# =================================================
# Start exercise request handling types
# =================================================


type _ProcessResponseDTO = OobResponseDTO[
    ExerciseStatusEnum,  # Domain status enumeration
    # FIXME: Replace TestExerciseCase
    TestExerciseMeta[OptionMetaDTO],  # Template exercise data
    dict[str, Any],  # Extra context for template
]
type _ProcessHandler = RequestHandler[
    NullProtocol,  # No request parameters
    RequestContextProtocol,  # Authentication required
    RequestDataProtocol[dict[str, str]],  # Request data
    NullProtocol,  # Validated data
    UserCommandProtocol,  # Execute use case by user command
    tuple[
        TestExerciseMeta[OptionMetaDTO],
        TestExerciseMeta[OptionMetaDTO],
    ],  # Domain result
    _ProcessResponseDTO,  # Response data for template
]

# =================================================
# Implementation
# =================================================

HANDLERS = MainContainer.lang.handlers


class RegularTranslationTestPerformView(
    ExercisePerformView[
        _StartHandler,
        _StartResponseDTO,
        _ProcessHandler,
        _ProcessResponseDTO,
    ]
):
    """Regular translation test exercise performing view."""

    TEMPLATE_PATH = 'lang/exercise/test/'
    template_name = 'lang/exercise/test/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        start_handler: _StartHandler = Provide[
            HANDLERS.start_regular_translation_test  # type: ignore[attr-defined]
        ],
        process_handler: _ProcessHandler = Provide[
            HANDLERS.process_regular_translation_test  # type: ignore[attr-defined]
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
        result = self.process_handler.execute(
            params=NullDTO(),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
        return result
