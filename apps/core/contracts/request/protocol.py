"""Request protocols."""

from typing import Protocol, TypeVar

ActionT = TypeVar('ActionT')


class HasAction(Protocol[ActionT]):
    """Protocol for has *action* interface."""

    action: ActionT
