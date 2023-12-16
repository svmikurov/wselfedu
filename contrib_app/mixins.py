from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class HandleNoPermissionMixin:
    """
    Add a redirect url and a message,
    if the user doesn't have permission.
    """
    message_no_permission = 'У вас нет разрешения на эти действия'
    url_no_permission = reverse_lazy('home')

    def handle_no_permission(self):
        messages.error(self.request, self.message_no_permission)
        return redirect(self.url_no_permission)


class CheckUserForOwnershipAccountMixin(UserPassesTestMixin):
    """
    Check if the user has owner permission on account.
    """
    message_no_permission = 'У вас нет разрешения на эти действия'
    url_no_permission = reverse_lazy('home')

    def authorship_check(self):
        current_user = self.get_object()
        specified_user = self.request.user

        if not self.request.user.is_authenticated:
            return False
        elif current_user != specified_user:
            return False
        elif current_user == specified_user:
            return True

    def get_test_func(self):
        return self.authorship_check
