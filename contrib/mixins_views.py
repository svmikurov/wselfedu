"""
Django views mixins.
"""

from typing import Callable, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView


class FormMessageMixin:
    """Add a flash message at form submission."""

    success_message = 'Успех!'
    """Success action message text (`str`).
    """
    error_message = 'Ошибка!'
    """Error action message text (`str`).
    """

    def form_valid(self, form: Form) -> HttpResponse:
        """Add success message to valid form.

        Parameters
        ----------
        form : `django.forms.Form`
            Django form instance.

        Returns
        -------
        response : `HttpResponse`
            An HTTP response.
        """
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form: Form) -> HttpResponse:
        """Add error message to invalid form.

        Parameters
        ----------
        form : `django.forms.Form`
            Django form instance.

        Returns
        -------
        response : `HttpResponse`
            An HTTP response.
        """
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response


class HandleNoPermissionMixin:
    """Add a redirect url and a message, if the user doesn't have
    permission to perform an action.
    """

    message_no_permission = 'Для доступа необходимо войти в приложение'
    """Message no permission (`str`).
    """
    url_no_permission = reverse_lazy('users:login')
    """Path schema for redirecting a user without permissions (`str`).
    """

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.message_no_permission)
        return redirect(self.url_no_permission)


class CheckUserOwnershipMixin(
    HandleNoPermissionMixin,
    FormMessageMixin,
    UserPassesTestMixin,
):
    """Checking user ownership of an object."""

    def check_ownership(self) -> bool:
        """Check if the user is the owner of the object.

        Returns
        -------
        `bool`
            Return the `True` if the user is the owner of the object,
            otherwise return the `False`.
        """
        current_user = self.request.user
        specified_user = self.get_object().user
        return current_user == specified_user

    def get_test_func(self) -> Callable:
        """Return the test result.

        This is an interface UserPassesTestMixin method override."""
        return self.check_ownership


class CheckObjectOwnershipMixin(
    HandleNoPermissionMixin,
    UserPassesTestMixin,
):
    """Checking user ownership of an object."""

    def check_ownership(self) -> bool:
        """Check if the user is the owner of the object."""
        current_user = self.request.user
        specified_user = self.get_object()
        return current_user == specified_user

    def get_test_func(self) -> Callable:
        """Return the test result.

        This is an interface UserPassesTestMixin method override."""
        return self.check_ownership


class CheckAdminMixin(HandleNoPermissionMixin, UserPassesTestMixin):
    """Check current user for admin permissions."""

    def check_admin(self) -> bool:
        if self.request.user.is_superuser:
            return True
        else:
            self.message_no_permission = 'Нужны права администратора'
            return False

    def get_test_func(self) -> Callable:
        """Return the test result.

        This is an interface UserPassesTestMixin method override."""
        return self.check_admin


class ObjectDeleteErrorMixin:
    """Tell if triggered object delete protect.

    Apply redirect url and message when raise ProtectedError.
    """

    protected_redirect_url = 'home'
    protected_message = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )

    def post(
        self,
        request: HttpRequest,
        *args: object,
        **kwargs: object,
    ) -> HttpResponse:
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_redirect_url)


class CheckLoginPermissionMixin(
    HandleNoPermissionMixin,
    FormMessageMixin,
    LoginRequiredMixin,
):
    """Verify that the current user is authenticated. If not, display
    a message and redirect to the login page."""


class PermissionProtectDeleteView(
    ObjectDeleteErrorMixin,
    CheckUserOwnershipMixin,
    DeleteView,
):
    """Preventing deletion of a protected object view."""


class ReuseSchemaFilterQueryMixin(MultipleObjectMixin):
    """Reuses previous url schema filter query with pagination.

    Adds ``reused_query`` to the URL scheme query.

    Example
    -------
    .. code-block::

       <a href="?{{reused_query}}&page={{page_obj.next_page_number}}">
         next page
       </a>

    .. # noqa: E501
    """

    @staticmethod
    def get_schema_query(request: HttpRequest, keys: tuple[str, ...]) -> str:
        """Get schema query by specific keys in request."""
        querydict = request.GET
        queries = []
        for key, value in querydict.items():
            if key in keys or value:
                queries.append('='.join((key, value)))
        return '&'.join(queries)

    def get_context_data(self, **kwargs: object) -> Dict[str, object]:
        """Insert the ``reused_query`` into the context dict.

        Parameters
        ----------
        **kwargs : object
            Context data.

        Returns
        -------
        context : Dict[str, object]
            Template context with
        """
        context = super().get_context_data(**kwargs)
        filter_fields = self.filterset_class.get_filter_fields()
        context['reused_query'] = self.get_schema_query(
            self.request,
            filter_fields,
        )
        return context


class ReuseSchemaQueryFilterView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ReuseSchemaFilterQueryMixin,
    FilterView,
):
    """Filter view with pagination."""
