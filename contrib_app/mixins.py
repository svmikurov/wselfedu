from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.list import MultipleObjectMixin
from django_filters.views import FilterView

NO_ADMIN_PERMISSION_MSG = 'Нужны права администратора'
NO_ADMIN_PERMISSION_URL = 'users/login/'

MESSAGE_NO_PERMISSION = 'Для доступа необходимо войти в приложение'
"""Message to the user if they do not have permission to perform the action.
"""
URL_NO_PERMISSION = 'users:login'
"""The name of the URL redirect for the user if they do not have permission to
perform the action.
"""
PROTECTED_REDIRECT_URL = 'home'
"""Redirect path name when deleting a model instance if its relationship is
protected from deletion.
"""
PROTECTED_MESSAGE = ('Невозможно удалить этот объект, так как он используется '
                     'в другом месте приложения')
"""Message when deleting a model instance if its relationship is protected from
deletion.
"""


class HandleNoPermissionMixin:
    """Add a redirect url and a message, if the user doesn't have permission.
    """

    message_no_permission = MESSAGE_NO_PERMISSION
    url_no_permission = reverse_lazy(URL_NO_PERMISSION)

    def handle_no_permission(self):
        messages.error(self.request, self.message_no_permission)
        return redirect(self.url_no_permission)


class CheckUserOwnershipMixin(UserPassesTestMixin):
    """Check if the user has owner permission on account."""

    def authorship_check(self):
        current_user = self.get_object()
        specified_user = self.request.user

        if current_user == specified_user:
            return True

    def get_test_func(self):
        return self.authorship_check


class CheckObjectOwnershipMixin(UserPassesTestMixin):
    """Check if the user has owner permission on object."""

    def authorship_check(self):
        current_user = self.request.user
        specified_user = self.get_object().user

        if current_user == specified_user:
            return True

    def get_test_func(self):
        return self.authorship_check


class CheckUserPkForOwnershipAccountMixin(UserPassesTestMixin):
    """Check if the user has owner permission on account."""

    def check(self):
        url_kwargs = self.request.resolver_match.captured_kwargs
        if self.request.user.id == url_kwargs.get('pk'):
            return True

    def get_test_func(self):
        return self.check


class AccountOwnershipMixin(
    HandleNoPermissionMixin,
    CheckUserOwnershipMixin,
):
    """
    Check if the user has owner permission on account.
    Add a redirect url and a message, if the user doesn't have permission.
    """


class UserPassesTestAdminMixin(UserPassesTestMixin):
    """Check current user for admin permissions."""

    def admin_check(self):
        if self.request.user.is_superuser:
            return True
        else:
            self.message_no_permission = NO_ADMIN_PERMISSION_MSG
            return False

    def get_test_func(self):
        return self.admin_check


class AddMessageToFormSubmissionMixin:
    """Add a flash message on form submission."""

    success_message = 'Успех!'
    error_message = 'Ошибка!'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, self.error_message)
        return response


class RedirectForModelObjectDeleteErrorMixin:
    """
    Add protected_redirect_url when raise ProtectedError.
    Add protected_message when raise ProtectedError.
    """
    protected_redirect_url = PROTECTED_REDIRECT_URL
    protected_message = PROTECTED_MESSAGE

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_redirect_url)


class ReuseSchemaFilterQueryMixin(MultipleObjectMixin):
    """Reuses the previous schema filter query mixin."""

    def get_schema_filter_query(self):
        """Create schema filter query for reuse in filter."""
        filter_fields = self.filterset_class.get_filter_fields()
        querydict = self.request.GET
        queries = []
        for field, value in querydict.items():
            if field in filter_fields or value:
                queries.append('='.join((field, value)))
        return '&'.join(queries)

    def get_context_data(self, **kwargs):
        """Add schema filter query to context."""
        context = super().get_context_data(**kwargs)
        context['reused_query'] = self.get_schema_filter_query()
        return context


class CheckObjectPermissionMixin(
    HandleNoPermissionMixin,
    CheckObjectOwnershipMixin,
    AddMessageToFormSubmissionMixin,
):
    """"""


class CheckLoginPermissionMixin(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessageToFormSubmissionMixin,
):
    """"""


class PermissionProtectDeleteView(
    HandleNoPermissionMixin,
    CheckObjectOwnershipMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    """"""


class ReuseSchemaQueryFilterView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    ReuseSchemaFilterQueryMixin,
    FilterView,
):
    """"""
