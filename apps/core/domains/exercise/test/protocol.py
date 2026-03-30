"""Test exercise interface."""

from typing import Protocol

from .. import protocol


class HasOptionValue(Protocol):
    """Protocol for has *option value* interface."""

    option_value: int


class HasOptionCount(Protocol):
    """Protocol for item option count object interface."""

    option_count: int


class OptionProtocol(
    HasOptionValue,
    protocol.HasText,
    Protocol,
):
    """Protocol for option DTO."""


class OptionMetaProtocol(
    protocol.HasResourceIdentifier,
    HasOptionValue,
    protocol.HasDefineText,
    protocol.HasExplainText,
    Protocol,
):
    """Protocol for option meta data."""


# =================================================
# Test exercise parameters DTO interface
# =================================================


class TestExerciseConfigProtocol(
    protocol.HasItemCount,
    protocol.HasDisplayOrder,
    HasOptionCount,
    Protocol,
):
    """Test exercise perform configuration DTO interface."""


# =================================================
# Test exercise case DTO interface
# =================================================


class TestExerciseCaseProtocol(
    protocol.HasExerciseStatus,
    Protocol,
):
    """Test exercise case DTO interface."""
