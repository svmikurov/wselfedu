"""Core app mixins."""

from typing import Generic, TypeVar

T = TypeVar('T')


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
