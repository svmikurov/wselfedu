"""Defines adapter."""

from ._abc_output import IOutputPort


class ConsoleOutputAdapter(IOutputPort):
    """Terminal output."""

    def show_result(self, result: float) -> None:
        """Show result in terminal."""
        print(f'Result: {result}')
