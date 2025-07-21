"""Defines external adapters."""

from ...ports.external import IOutputPort


class ConsoleOutput(IOutputPort):
    """Console output adapter."""

    def show_result(self, result: float) -> None:
        """Output result to console."""
        print(f'Result: {result}')


class GuiOutput(IOutputPort):
    """GUI output adapter (stub)."""

    def show_result(self, result: float) -> None:
        """Show result."""
        pass  # GUI implementation would go here
