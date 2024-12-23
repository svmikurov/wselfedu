"""User profile views."""

from django.views.generic import DetailView

from contrib.views.general import CheckObjectOwnershipMixin
from users.models import UserApp


class UserDetailView(CheckObjectOwnershipMixin, DetailView):
    """User detail view."""

    template_name = 'users/profile.html'
    model = UserApp
