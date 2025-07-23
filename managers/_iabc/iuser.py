"""Defines protocol and abc for user model manager."""

from typing import Protocol, TypeVar

from apps.users.models import CustomUser

UserT_co = TypeVar('UserT_co', bound=CustomUser, covariant=True)
UserManagerT_co = TypeVar(
    'UserManagerT_co',
    bound='IUserManager[CustomUser]',
    covariant=True,
)


class IUserManager(Protocol[UserT_co]):
    """Protocol for user model manager interface."""
