"""Core app view mixins."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypedDict, TypeVar

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateResponseMixin

from .abstract import AbstractProcessAction, AbstractStartAction

if TYPE_CHECKING:
    from django.http import HttpRequest


T = TypeVar('T')

StartHandlerT = TypeVar('StartHandlerT')
ProcessHandlerT = TypeVar('ProcessHandlerT')

ResponseDtoT = TypeVar('ResponseDtoT')
OobResponseDtoT = TypeVar('OobResponseDtoT')


class InitialHtmlContextT(TypedDict, total=False):
    """Initial html context typed dict."""

    initial_html: str


class GetUseCaseMixin(Generic[T]):
    """Get use case mixin."""

    _use_case: T | None = None

    @property
    def use_case(self) -> T:
        """Get use case."""
        if self._use_case is None:
            raise AttributeError('UseCase not initialized')
        return self._use_case


class GetServiceMixin(Generic[T]):
    """Get service mixin."""

    _service: T | None = None

    @property
    def service(self) -> T:
        """Get service."""
        if self._service is None:
            raise AttributeError('Service not initialized')
        return self._service


class GetRepositoryMixin(Generic[T]):
    """Get repository mixin."""

    _repository: T | None = None

    @property
    def repository(self) -> T:
        """Get repository."""
        if self._repository is None:
            raise AttributeError('Repository not initialized')
        return self._repository


class GetHandlerMixin(Generic[T]):
    """Mixin provides request handler."""

    _handler: T | None = None

    @property
    def handler(self) -> T:
        """Get request handler."""
        if self._handler is None:
            raise AttributeError('Request handler not initialized')
        return self._handler


# =================================================
# Handler mixins
# =================================================


class StartExerciseHandlerMixin(Generic[StartHandlerT]):
    """Mixin provides start exercise handler."""

    _start_handler: StartHandlerT | None

    @property
    def start_handler(self) -> StartHandlerT:
        """Get start exercise request handler."""
        if self._start_handler is None:
            raise AttributeError(
                'Start exercise request handler not initialized'
            )
        return self._start_handler


class ProcessExerciseHandlerMixin(Generic[ProcessHandlerT]):
    """Mixin provides exercise process handler."""

    _process_handler: ProcessHandlerT | None

    @property
    def process_handler(self) -> ProcessHandlerT:
        """Get exercise process handler."""
        if self._process_handler is None:
            raise AttributeError('Process exercise handler not initialized')
        return self._process_handler


# =================================================
# Request's method mixins
# =================================================


class AbstractPartialTemplateMixin(ABC, Generic[ResponseDtoT]):
    """ABC for get partial html interface."""

    @abstractmethod
    def _get_partial_html(
        self,
        request: HttpRequest,
        schema: ResponseDtoT,
    ) -> str:
        """Get partial html."""


class ProcessHandlerTemplateMixin(
    TemplateResponseMixin,
    AbstractPartialTemplateMixin[ResponseDtoT],
    AbstractStartAction[ResponseDtoT],
    ABC,
    Generic[ResponseDtoT],
):
    """Provides handler process with template rendering."""

    def get(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render initial template with process handler result."""
        result = self._start(**kwargs)

        if request.headers.get('HX-Request') == 'true':
            # Renders process handler result with partial template
            # if HTMX request.
            return HttpResponse(self._get_partial_html(request, result))

        else:
            # Renders process handler result with initial template.
            context: InitialHtmlContextT = {
                'initial_html': self._get_partial_html(request, result),
                **result.model_dump(),  # type: ignore
            }

            return render(request, self.get_template_names(), context)


class ProcessHandlerPartialTemplateMixin(
    TemplateResponseMixin,
    AbstractPartialTemplateMixin[ResponseDtoT],
    AbstractProcessAction[ResponseDtoT],
    ABC,
    Generic[ResponseDtoT],
):
    """Provides handler process with partial template rendering."""

    def post(self, request: HttpRequest, **kwargs: object) -> HttpResponse:
        """Render partial template with process handler result."""
        result = self._process(**kwargs)
        return HttpResponse(self._get_partial_html(request, result))
