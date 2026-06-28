"""Django site exceptions."""


class SuspiciousOperation(Exception):
    """The user did something suspicious."""


class ValidationError(Exception):
    """Raised then validation error."""
