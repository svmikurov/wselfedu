"""Admin interface of models representation."""

from django.contrib import admin

from config.constants import PK, USERNAME
from users.models import Mentorship, MentorshipRequest, UserApp


@admin.register(UserApp)
class UserAdmin(admin.ModelAdmin):
    """Representation of Users model."""

    list_display = [PK, USERNAME, 'is_staff', 'date_joined']
    ordering = ['date_joined']
    list_display_links = [USERNAME]


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    """Representation of Mentorship model."""


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    """Representation of MentorshipRequest model."""
