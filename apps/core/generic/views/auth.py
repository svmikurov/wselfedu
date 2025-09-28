"""Check user authentication a view mixins."""

from typing import Generic, TypeVar

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.db.models.query import QuerySet

ObjectT = TypeVar('ObjectT', bound=models.Model)


class OwnershipRequiredMixin(
    LoginRequiredMixin,
    UserPassesTestMixin,
    Generic[ObjectT],
):
    """Verify that the current user is ownership of query object."""

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
        return bool(self.request.user == self.get_object().user)  # type: ignore[attr-defined]
