"""User profile views module."""

from django.views.generic import DetailView

from contrib.mixins_views import CheckObjectOwnershipMixin
from users.models import UserModel


class UserDetailView(CheckObjectOwnershipMixin, DetailView):
    """User detail view."""

    template_name = 'users/profile.html'
    model = UserModel
