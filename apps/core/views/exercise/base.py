"""Base exercise view."""

from typing import Any, Generic, TypeAlias, TypeVar

from django.http import HttpRequest, HttpResponse
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from apps.core.handlers.dto import (
    DetailRequestParams,
    QueryRequestParams,
    RequestContext,
    RequestData,
)
from apps.core.handlers.protocol import RequestHandlerProtocol
from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin
from apps.users.models import Person
from contracts.entity.response.base import (
    OobResponseProtocol,
)
from contracts.enums.exercise import ExerciseStatus
from contracts.schemas.response.generic import OobResponseDTO

from ..mixins import (
    ProcessHandlerPartialTemplateMixin,
    ProcessHandlerTemplateMixin,
)
from .mixins import ExerciseLoopMixin, ExercisePartialTemplateMixin

__all__ = ('ExercisePerformView',)


# DEPRECATED: Remove type alias after implementation deletion
_OobResponseDtoT: TypeAlias = OobResponseDTO[object, object, object]

HandlerT = TypeVar('HandlerT')
ResponseDtoT = TypeVar(
    'ResponseDtoT',
    bound=OobResponseProtocol[ExerciseStatus],
)

# DEPRECATED: Remove type alias after implementation deletion
ProcessHandlerT = RequestHandlerProtocol[Any, Any, Any, _OobResponseDtoT]


class ExercisePerformView(
    UserLoginRequiredMixin,
    GetHandlerMixin[HandlerT],
    ExercisePartialTemplateMixin[ResponseDtoT],
    ProcessHandlerTemplateMixin[ResponseDtoT],
    ProcessHandlerPartialTemplateMixin[ResponseDtoT],
    View,
    Generic[HandlerT, ResponseDtoT],
):
    """Base exercise performing view."""


# IDEA: Relocate OOB creating to response adapter
class IdeaExercisePerformView(
    UserLoginRequiredMixin,
    GetHandlerMixin[HandlerT],
    ExerciseLoopMixin,
    TemplateResponseMixin,
    View,
    Generic[HandlerT],
):
    """Base exercise performing view."""

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial template with process handler result."""
        result = self._start(**kwargs)

        if request.headers.get('HX-Request') == 'true':
            return HttpResponse(result)
        else:
            raise NotImplementedError

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render partial template with process handler result."""
        result = self._process(**kwargs)
        return HttpResponse(result)


# DEPRECATED: Remove, use `ExercisePerformView`
# with process action mixins
class QueryExercisePerformMixin:
    """Provides query exercise perform."""

    user: Person
    request: HttpRequest
    start_handler: ProcessHandlerT

    def _start(self, **kwargs: object) -> _OobResponseDtoT:
        return self.start_handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _OobResponseDtoT:
        return self.process_handler.execute(  # type: ignore
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )


# DEPRECATED: Remove, use `ExercisePerformView`
# with process action mixins
class DetailExercisePerformMixin:
    """Provides detail exercise perform."""

    user: Person
    request: HttpRequest
    start_handler: ProcessHandlerT

    def _start(self, **kwargs: object) -> _OobResponseDtoT:
        return self.start_handler.execute(
            params=DetailRequestParams(pk=kwargs['pk']),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _OobResponseDtoT:
        return self.process_handler.execute(  # type: ignore
            params=DetailRequestParams(pk=int(kwargs['pk'])),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
