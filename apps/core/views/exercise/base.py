"""Base exercise view."""

from typing import Any, Generic, TypeVar

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateResponseMixin

from apps.core.views.auth import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin, IsHtmxMixin
from apps.users.models import Person
from ports.contract.entity.domain.general import DumpModelProtocol
from ports.contract.enums.exercise import ExerciseStatus
from ports.contract.infra.handler import RequestHandlerProtocol
from ports.contract.response.web import HtmlResponseProtocol
from ports.interfaces.schemas.request.handler import (
    DetailRequestParams,
    QueryRequestParams,
    RequestContext,
    RequestData,
)

from .mixins import ExerciseLoopMixin

__all__ = ('ExercisePerformView',)


HandlerT = TypeVar('HandlerT')
_DTO = DumpModelProtocol[dict[str, str]]
_Response = HtmlResponseProtocol[ExerciseStatus, _DTO, _DTO]
ResponseDtoT = TypeVar('ResponseDtoT', bound=_Response)


# DEPRECATED: Remove type alias after implementation deletion
ProcessHandlerT = RequestHandlerProtocol[Any, Any, Any, Any]


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
        return HttpResponse(self._process(**kwargs).html)


# DEPRECATED: Remove, use `ExercisePerformView`
# with process action mixins
class QueryExercisePerformMixin:
    """Provides query exercise perform."""

    user: Person
    request: HttpRequest
    start_handler: ProcessHandlerT

    def _start(self, **kwargs: object) -> _Response:
        return self.start_handler.execute(  # type: ignore
            params=QueryRequestParams(query=self.request.GET.dict()),
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _Response:
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

    def _start(self, **kwargs: object) -> _Response:
        return self.start_handler.execute(  # type: ignore
            params=DetailRequestParams(pk=kwargs['pk']),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data={}),
        )

    def _process(self, **kwargs: object) -> _Response:
        return self.process_handler.execute(  # type: ignore
            params=DetailRequestParams(pk=int(kwargs['pk'])),  # type: ignore
            context=RequestContext(user=self.user),
            data=RequestData(data=self.request.POST.dict()),
        )
