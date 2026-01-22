"""Check user authentication a view mixins."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Generic, TypeVar

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Model

from apps.users.models import Person

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

__all__ = [
    'UserRequestMixin',
    'UserLoginRequiredMixin',
    'OwnerMixin',
    'OwnershipRequiredMixin',
]

M = TypeVar('M', bound=Model)


class UserRequestMixin:
    """Provides the user who sent the request."""

    @cached_property
    def user(self) -> Person:
        """Get user who sent the request."""
        if not isinstance(self.request.user, Person):  # type: ignore[attr-defined]
            raise TypeError('User type error')
        return self.request.user  # type: ignore[attr-defined]


class UserLoginRequiredMixin(
    UserRequestMixin,
    LoginRequiredMixin,
):
    """Mixin provides authenticated user."""


class OwnerMixin:
    """Provides object owner."""

    def _get_owner(self) -> Person:
        return self.get_object().user  # type: ignore[no-any-return, attr-defined]


class OwnershipRequiredMixin(
    UserLoginRequiredMixin,
    UserPassesTestMixin,
    Generic[M],
):
    """Verify that the current user is owner of query object."""

    _object: M | None = None

    def get_object(
        self,
        queryset: QuerySet[M] | None = None,
    ) -> M:
        """Cache the object after the first query."""
        if self._object is None:
            self._object = super().get_object(queryset)  # type: ignore[misc]
        return self._object

    def test_func(self) -> bool:
        """Check that user is object owner."""
        return bool(self.user == self.get_object().user)  # type: ignore[attr-defined]
