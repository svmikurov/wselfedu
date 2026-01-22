"""Base edit views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from django.db.models import Model
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from .auth import OwnershipRequiredMixin, UserLoginRequiredMixin

if TYPE_CHECKING:
    from django.db.models.query import QuerySet
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

M = TypeVar('M', bound=Model)


class CsrfProtectMixin:
    """Mixin provides CSRF protection."""

    @method_decorator(csrf_protect)
    def dispatch(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponseBase:
        """Add CSRF protection."""
        return super().dispatch(request, *args, **kwargs)  # type: ignore[misc, no-any-return]


class UserActionKwargsFormMixin:
    """Mixin provides user and form action kwargs for form."""

    request: HttpRequest

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add data to form kwargs."""
        kwargs = super().get_form_kwargs()  # type: ignore[misc]
        kwargs['form_action'] = self.request.path
        kwargs['user'] = self.user  # type: ignore[attr-defined]
        return kwargs  # type: ignore[no-any-return]


class BaseAddView(UserLoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
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


class BaseListView(
    UserLoginRequiredMixin,
    CsrfProtectMixin,
    generic.ListView,  # type: ignore[type-arg]
    Generic[M],
):
    """Base list view provides CSRF protection."""

    def get_queryset(self) -> QuerySet[M]:
        """Get user's item list."""
        return (
            super()
            .get_queryset()
            .filter(user=self.user)
            .order_by('-created_at')
        )


class BaseCreateView(
    UserLoginRequiredMixin,
    UserActionKwargsFormMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Base create view."""


class BaseUpdateView(
    UserActionKwargsFormMixin,
    OwnershipRequiredMixin[M],
    generic.UpdateView,  # type: ignore[type-arg]
    Generic[M],
):
    """Base update view provides ownership protection."""
