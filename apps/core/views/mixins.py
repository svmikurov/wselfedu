"""Core app mixins."""

from typing import Generic, TypeVar

T = TypeVar('T')

StartHandler = TypeVar('StartHandler')
ProcessHandler = TypeVar('SolveHandler')


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
# Exercise mixins
# =================================================


class StartExerciseHandlerMixin(Generic[StartHandler]):
    """Mixin provides start exercise handler."""

    _start_handler: StartHandler | None

    @property
    def start_handler(self) -> StartHandler:
        """Get start exercise request handler."""
        if self._start_handler is None:
            raise AttributeError(
                'Start exercise request handler not initialized'
            )
        return self._start_handler


class ProcessExerciseHandlerMixin(Generic[ProcessHandler]):
    """Mixin provides exercise process handler."""

    _process_handler: ProcessHandler | None

    def process_handler(self) -> ProcessHandler:
        """Get exercise process handler."""
        if self._process_handler is None:
            raise AttributeError('Process exercise handler not initialized')
        return self._process_handler
