"""Language application views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from dependency_injector.wiring import Provide, inject
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin, TemplateResponseMixin

from wse.di.site import DjangoSiteContainer
from wse.domain.enums import ExerciseAction
from wse.site import dtos
from wse.site.protocols import HtmlResponsible

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.http.response import HttpResponseBase


T = TypeVar('T')
HandlerT = TypeVar('HandlerT')
ResponseT = TypeVar('ResponseT', bound=HtmlResponsible)


class SuspiciousOperation(Exception):
    """The user did something suspicious."""


class ExercisePerformView(
    TemplateResponseMixin,
    ContextMixin,
    View,
    Generic[HandlerT, ResponseT],
):
    """Exercise performing view."""

    template_name = 'exercise.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: HandlerT = Provide[DjangoSiteContainer.testing],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    ###############################################
    # Request methods
    ###############################################

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial template with process handler result."""
        result = self._start(**kwargs)

        if self.is_htmx:
            return HttpResponse(result.html)
        else:
            return render(
                request,
                self.get_template_names(),
                result,
            )

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render partial template with process handler result."""
        return HttpResponse(self._process(**kwargs).html)

    ###############################################
    # Handler call
    ###############################################

    def _start(self, **kwargs: object) -> ResponseT:
        return self.handler.execute(  # type: ignore
            params=dtos.NullDTO(),
            context=dtos.RequestContext(),
            data=dtos.RequestData(data={'action': ExerciseAction.CREATE_TASK}),
        )

    def _process(self, **kwargs: object) -> ResponseT:
        if not self.is_htmx:
            raise SuspiciousOperation(
                'POST requests for exercise processing must be HTMX requests'
            )

        return self.handler.execute(  # type: ignore
            params=dtos.NullDTO(),
            context=dtos.RequestContext(),
            data=dtos.RequestData(data=self.request.POST.dict()),
        )

    ###############################################
    # Properties
    ###############################################

    @property
    def is_htmx(self) -> bool:
        """Is HTMX request."""
        return bool(self.request.headers.get('HX-Request') == 'true')

    @property
    def handler(self) -> HandlerT:
        """Request handler."""
        if self._handler is None:
            raise AttributeError('Request handler not initialized')
        return self._handler
