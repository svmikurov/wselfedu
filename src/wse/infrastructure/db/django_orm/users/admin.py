"""Users application model administration."""

from django.contrib import admin

from .models import Person


@admin.register(Person)
class Person(admin.ModelAdmin):  # type: ignore[no-redef, type-arg]
    """Person model administration."""

    list_display = ['username', 'date_joined']
    ordering = ['username']
