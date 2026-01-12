"""Base views for language rule."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from functools import cached_property
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from dependency_injector.wiring import Provide, inject
from django.core.exceptions import BadRequest, PermissionDenied
from django.http.response import Http404
from django.views import generic

from apps.core.views.auth import UserRequestMixin
from apps.lang import models
from di import MainContainer

if TYPE_CHECKING:
    from dependency_injector.providers import Container
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

    from apps.lang.adapters import WebRuleAdapterABC
    from apps.lang.di import LanguageContainer
    from apps.lang.repositories import RuleRepositoryABC

    type ContainerDI = Container[LanguageContainer]

logger = logging.getLogger(__name__)

CONTAINER: ContainerDI = MainContainer.lang

T = TypeVar('T')


class BaseRuleDetailView(
    UserRequestMixin,
    generic.TemplateView,
    ABC,
    Generic[T],
):
    """Base view for rule details with common error handling.

    Alternative to UseCase pattern.

    Implements Template Method Pattern with Hook Operations
    to provide common error handling, validation,
    and dependency injection while allowing subclasses
    to define specific data retrieval and conversion logic.

    Subclasses must implement:
    - `_get_rule_object()` - retrieve domain object
    - `_convert_to_dto()` - convert to presentation layer

    Hooks available for extension (empty by default):
    - `_before_get_object()` - pre-processing
    - `_after_get_object()` - post-retrieval logic
    - `_after_convert_to_dto()` - DTO modification
    - `_validate_result()` - final validation

    For typical Django views without complex processing, consider using
    standard Django Class-Based Views. This pattern is appropriate for:
    - Complex business logic workflows
    - Multiple similar views with shared error handling
    - Code reuse across different DTO representations
    - Learning OOP and design patterns

    This implementation demonstrates:
    - Template Method Pattern (GoF)
    - Dependency Injection Principle
    - Inversion of Control (IoC)
    - Hook Methods for extensibility
    - Separation of Concerns (SoC)
    """

    _repository: RuleRepositoryABC | None = None
    _adapter: WebRuleAdapterABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: RuleRepositoryABC = Provide[CONTAINER.rule_repository],
        adapter: WebRuleAdapterABC = Provide[CONTAINER.rule_web_adapter],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject the dependencies."""
        self._repository = repository
        self._adapter = adapter
        return super().dispatch(request, *args, **kwargs)

    @property
    def repository(self) -> RuleRepositoryABC:
        """Get validated repository."""
        if self._repository is None:
            raise AttributeError('Repository not initialized')
        return self._repository

    @property
    def adapter(self) -> WebRuleAdapterABC:
        """Get validated adapter."""
        if self._adapter is None:
            raise AttributeError('Adapter not initialized')
        return self._adapter

    @cached_property
    def rule_pk(self) -> int:
        """Extract and validate rule primary key."""
        try:
            return int(self.kwargs['pk'])
        except (ValueError, KeyError, TypeError) as e:
            raise BadRequest(
                f'Invalid rule ID: {self.kwargs.get("pk")}'
            ) from e

    @cached_property
    def rule(self) -> T:
        """Get rule data with common error handling.

        Template Method Pattern.
        """
        try:
            # Pre-processing (hooks)
            self._before_get_object()

            # Basic steps
            rule_object = self._get_rule_object()
            self._after_get_object(rule_object)

            rule_dto = self._convert_to_dto(rule_object)
            self._after_convert_to_dto(rule_dto)

            # Result validation
            self._validate_result(rule_dto)

            return rule_dto

        except models.Rule.DoesNotExist as e:
            raise Http404(f'Rule with pk={self.rule_pk} not found') from e

        except PermissionDenied:
            raise

        except ValueError as e:
            raise BadRequest(str(e)) from e

        except Exception as e:
            logger.error(
                (
                    f'Unexpected error in {self.__class__.__name__} '
                    f'for rule {self.rule_pk}: {e}'
                ),
                exc_info=True,
            )
            raise

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add data to context."""
        context = super().get_context_data(**kwargs)
        context['rule'] = self.rule
        return context

    # ----------------
    # Abstract methods
    # ----------------

    @abstractmethod
    def _get_rule_object(self) -> models.Rule:
        """Get rule object from repository. Implement in subclass."""

    @abstractmethod
    def _convert_to_dto(self, rule_object: models.Rule) -> T:
        """Convert rule object to DTO. Implement in subclass."""

    # ------------
    # Hook-methods
    # ------------

    def _before_get_object(self) -> None:
        """Call before getting rule object. Override if needed."""
        pass

    def _after_get_object(self, rule_object: models.Rule) -> None:
        """Call after getting rule object. Override if needed."""
        pass

    def _after_convert_to_dto(self, rule_dto: T) -> None:
        """Call after converting to DTO. Override if needed."""
        pass

    def _validate_result(self, rule_dto: T) -> None:
        """Validate DTO before returning. Override if needed."""
        pass
