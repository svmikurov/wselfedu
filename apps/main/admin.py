"""Contains Main application model administration."""

from django.contrib import admin

from .models import Discipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Administration of discipline model."""

    date_hierarchy = 'created_at'
    list_display = ['name', 'description', 'created_at']

    fields = ['name', 'description', 'created_at']
    readonly_fields = ['created_at']
