"""Modul of models representation in the admin interface."""

from django.contrib import admin

from users.models import Mentorship, MentorshipRequest, UserModel


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""

    list_display = ['pk', 'username', 'is_staff', 'date_joined']
    ordering = ['date_joined']
    list_display_links = ['username']


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):
    """Representation of model in the admin interface."""
