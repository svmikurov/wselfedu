"""Base exercise view."""

from typing import Any, Generic, TypeAlias, TypeVar

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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
from apps.core.views.mixins import GetHandlerMixin, IsHtmxMixin
from apps.users.models import Person
from contracts.entity.response.base import (
    HtmlResponseProtocol,
)
from contracts.enums.exercise import ExerciseStatus
from contracts.schemas.response.generic import HtmlResponseDTO

from .mixins import ExerciseLoopMixin

__all__ = ('ExercisePerformView',)


# DEPRECATED: Remove type alias after implementation deletion
_HtmlResponseDtoT: TypeAlias = HtmlResponseDTO[object, object, object]

HandlerT = TypeVar('HandlerT')
ResponseDtoT = TypeVar(
    'ResponseDtoT',
    bound=HtmlResponseProtocol[ExerciseStatus],
)

# DEPRECATED: Remove type alias after implementation deletion
ProcessHandlerT = RequestHandlerProtocol[Any, Any, Any, _HtmlResponseDtoT]


class ExercisePerformView(
    UserLoginRequiredMixin,
    IsHtmxMixin,
    GetHandlerMixin[HandlerT],
    ExerciseLoopMixin,
    TemplateResponseMixin,
    View,
    Generic[HandlerT],
):
    """Base exercise performing view."""

    # template

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial template with process handler result."""
        result = self._start(**kwargs)

        if self.is_htmx:
            return HttpResponse(result.html)
        else:
            return render(
                request,
                self.get_template_names(),
                result.context.model_dump(),
            )

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render partial template with process handler result."""
        return HttpResponse(self._process(**kwargs))


# DEPRECATED: Remove, use `ExercisePerformView`
# with process action mixins
class QueryExercisePerformMixin:
    """Provides query exercise perform."""

    user: Person
    request: HttpRequest
    start_handler: ProcessHandlerT

    def _start(self, **kwargs: object) -> _HtmlResponseDtoT:
        return self.start_handler.execute(
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _HtmlResponseDtoT:
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

    def _start(self, **kwargs: object) -> _HtmlResponseDtoT:
        return self.start_handler.execute(
            params=DetailRequestParams(pk=kwargs['pk']),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _HtmlResponseDtoT:
        return self.process_handler.execute(  # type: ignore
            params=DetailRequestParams(pk=int(kwargs['pk'])),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
