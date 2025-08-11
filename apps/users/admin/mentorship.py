"""Defines Users app model administration."""

from django.contrib import admin

from ..models import (
    Mentorship,
    MentorshipRequest,
)


@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Mentorship model representation."""

    list_display = ['mentor', 'student']
    ordering = ['mentor', 'student']


@admin.register(MentorshipRequest)
class MentorshipRequestAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Mentorship request model representation."""

    list_display = ['from_user', 'to_user']
    ordering = ['from_user', 'to_user']
