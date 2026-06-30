"""Domain layer exceptions."""


class DomainError(Exception):
    """Base domain exception."""

    pass


class NotEnoughLearnablesError(DomainError):
    """Raised when not enough learnables."""

    def __init__(self, required: int, actual: int) -> None:
        self.required = required
        self.actual = actual
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return (
            f'Not enough learnables. Required: {self.required}, '
            f'actual: {self.actual}'
        )


class EmptyLearnablesError(DomainError):
    """Raised when learnables is empty."""

    pass


class InvalidOptionCountError(DomainError):
    """Raises when testing exercise option count is invalid."""

    def __init__(
        self,
        option_count: int,
        min_option_count: int,
        max_option_count: int,
    ) -> None:
        self.option_count = option_count
        self.min_option_count = min_option_count
        self.max_option_count = max_option_count
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return (
            f'Option count must be between {self.min_option_count} '
            f'and {self.max_option_count}. Got: {self.option_count}'
        )
