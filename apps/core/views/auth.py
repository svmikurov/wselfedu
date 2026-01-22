"""Check user authentication a view mixins."""

from __future__ import annotations

from functools import cached_property
from typing import Generic, TypeVar

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.db.models.query import QuerySet

from apps.users.models import Person

ObjectT = TypeVar('ObjectT', bound=models.Model)


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
    Generic[ObjectT],
):
    """Verify that the current user is owner of query object."""

    _object: ObjectT | None = None

    def get_object(
        self,
        queryset: QuerySet[ObjectT] | None = None,
    ) -> ObjectT:
        """Cache the object after the first query."""
        if self._object is None:
            self._object = super().get_object(queryset)  # type: ignore[misc]
        return self._object

    def test_func(self) -> bool:
        """Check that user is object owner."""
        return bool(self.user == self.get_object().user)  # type: ignore[attr-defined]
