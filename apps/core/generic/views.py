"""Contains custom generic views."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import DeleteView

from apps.users.models import CustomUser


class HtmxDeleteView(UserPassesTestMixin, DeleteView):  # type: ignore[type-arg]
    """Delete the object with HTMX request."""

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        user = self.request.user
        if not isinstance(user, CustomUser):
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

    def _get_owner(self) -> CustomUser:
        raise NotImplementedError('Must implement `_get_owner()` in subclass')
