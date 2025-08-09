"""Defines Users app exceptions."""


class MentorshipError(Exception):
    """Raises when mentorship relationship errors.

    Args:
        message (str): Text error message for logging/debugging.
        html_message (str, optional):
            A message in HTML format for rendering in the interface.
            The default is 'message'.

    """

    def __init__(self, message: str, html_message: str | None = None) -> None:
        """Construct the exception."""
        super().__init__(message)
        # Standard error message
        self.message = message
        # Message to render in HTML
        self.html_message = html_message or message

    def __str__(self) -> str:
        """Return the string representation of exception."""
        return self.message
