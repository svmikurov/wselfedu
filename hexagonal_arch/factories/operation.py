"""Defines operation factory."""

from typing import Callable, Type

from ..enums import CalculateEnum
from ..ports.internal import IOperation


class OperationFactory:
    """Factory for Creating and Registering Calculator Entries."""

    _operation_registry: dict[CalculateEnum, Type[IOperation]] = {}

    @classmethod
    def register(
        cls, op_type: CalculateEnum
    ) -> Callable[[type[IOperation]], type[IOperation]]:
        """Registry  activity classes."""

        def decorator(
            op_class: Type[IOperation],
        ) -> Type[IOperation]:
            cls._operation_registry[op_type] = op_class
            return op_class

        return decorator

    @classmethod
    def create_operations(cls) -> dict[CalculateEnum, IOperation]:
        """Create operation instances."""
        return {
            op_type: op_class()
            for op_type, op_class in cls._operation_registry.items()
        }
