"""Contains custom generic views."""

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import DeleteView

from apps.users.models import Person


class OwnerMixin:
    """Mixin provides object owner."""

    def _get_owner(self) -> Person:
        return self.get_object().user  # type: ignore[no-any-return, attr-defined]


class HtmxDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,  # type: ignore[type-arg]
):
    """Delete the object with HTMX request."""

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        user = self.request.user
        if not isinstance(user, Person):
            return False
        return bool(user == self._get_owner())

    def delete(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        """Delete object with HTMX request."""
        self.object = self.get_object()
        self.object.delete()
        # HTMX does not update the template with response status 204
        return HttpResponse(status=200)

    def _get_owner(self) -> Person:
        raise NotImplementedError('Must implement `_get_owner()` in subclass')


class HtmxOwnerDeleteView(OwnerMixin, HtmxDeleteView):
    """Delete the object with HTMX request by owner."""
