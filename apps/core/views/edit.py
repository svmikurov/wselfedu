"""Base edit views."""

from typing import Any

from django.views import generic

from .auth import UserRequestMixin


class BaseAddView(UserRequestMixin, generic.FormView):  # type: ignore[type-arg]
    """Base view to add related entities via form.

    Override `form_class` attribute.

    `pk` - identifier of the entity to which the added entity is bound
    `user` - owner of relationship, the current user
    `form_action` - url path for POST request with filling form
    """

    template_name = 'components/crispy_form.html'
    form_class: Any | None = None

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add data to form."""
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk', None)
        kwargs['user'] = self.user
        kwargs['form_action'] = self.request.path
        return kwargs

    def get_success_url(self) -> str:
        """Get success url."""
        return self.request.path
