"""Defines user model manager."""

from django.db import models

from apps.users.models import CustomUser


class UserManager(models.Manager[CustomUser]):
    """User model manager."""

    def get_active_users(self) -> models.QuerySet[CustomUser]:
        """Get active users."""
        return (
            self
            .filter(is_active=True)
            .only('id', 'username')
        )  # fmt: skip
