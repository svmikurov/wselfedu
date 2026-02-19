"""User's profile view."""

from django.views.generic import TemplateView

from apps.core.views import ProfileMixin


class ProfileView(ProfileMixin, TemplateView):
    """User's profile view."""

    template_name = 'users/profile.html'
