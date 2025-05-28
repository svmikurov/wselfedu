"""Defines user profile views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    UpdateView,
)

User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view."""

    model = User
    template_name = 'profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """User edit profile view."""

    model = User
    fields = [
        'username',
    ]
    template_name = 'profile-edit.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_success_url(self) -> str:
        """Redirect to profile after processing a valid form."""
        return reverse_lazy(
            'profile',
            kwargs={'username': self.object.username},
        )

    def get_object(self, queryset: QuerySet | None = None) -> 'User':  # type: ignore
        """Get currently authenticated user for editing."""
        user = self.request.user
        if not user.is_authenticated:
            raise Http404('User not found')
        return user
