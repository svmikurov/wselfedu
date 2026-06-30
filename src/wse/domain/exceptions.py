"""Domain layer exceptions."""


class DomainError(Exception):
    """Base domain exception."""

    pass


class NotEnoughLearnablesError(DomainError):
    """Raised when not enough learnables."""

    pass


class EmptyLearnablesError(DomainError):
    """Raised when learnables is empty."""

    pass


class InvalidOptionCountError(DomainError):
    """Raises when testing exercise option count is invalid."""
