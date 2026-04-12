"""Protocol for Users app interface."""

from typing import Protocol

from .models import Person


class HasUser(Protocol):
    """Protocol for has user model interface."""

    user: Person
