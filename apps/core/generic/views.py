"""Contains custom generic views."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic import DeleteView


class HtmxDeleteView(UserPassesTestMixin, DeleteView):  # type: ignore[type-arg]
    """Delete the object with HTMX request."""

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        raise NotImplementedError()

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
