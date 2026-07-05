"""Domain constants."""

from dataclasses import dataclass

from . import exceptions


@dataclass(frozen=True)
class TaskConstraints:
    """Business constraints for exercise tasks."""

    MIN_OPTIONS: int = 2
    MAX_OPTIONS: int = 7

    @classmethod
    def validate_options(cls, option_count: int) -> None:
        """Validate option count against configured constraints.

        Raises:
            InvalidOptionCountError: If option_count < MIN_OPTIONS
                                     or option_count > MAX_OPTIONS.

        """
        if option_count < cls.MIN_OPTIONS or option_count > cls.MAX_OPTIONS:
            raise exceptions.InvalidOptionCountError(
                option_count, cls.MIN_OPTIONS, cls.MAX_OPTIONS
            )
