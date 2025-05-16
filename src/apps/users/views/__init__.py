"""User application views."""

__all__ = [
    'SignUpView',
    'ProfileView',
    'ProfileEditView',
]

from .auth_view import SignUpView
from .profile_views import ProfileEditView, ProfileView
