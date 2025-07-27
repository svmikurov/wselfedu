"""Defines mixins for admin panel."""

from django.http import HttpRequest


class UnchangeableAdminMixin:
    """Disabled edit of admin model fields."""

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable adding object."""
        return False

    def has_change_permission(
        self, request: HttpRequest, obj: object | None = None
    ) -> bool:
        """Disable change object."""
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: object | None = None
    ) -> bool:
        """Disable delete object."""
        return False
