"""Request handlers."""

from typing import Any


class ExerciseHandler:
    """Exercise performing request handler."""

    def execute(self, **data: object) -> dict[str, Any]:
        """Execute the exercise request."""
        print('DEBUG: Execute method called')
        return {'no_key': 'no_value'}
