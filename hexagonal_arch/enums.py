"""Defines operation enumerations."""

from enum import Enum


class CalculateEnum(Enum):
    """Supported calculation operations."""

    ADD = 'add'
    SUBTRACT = 'subtract'
    MULTIPLY = 'multiply'
    DIVIDE = 'divide'
