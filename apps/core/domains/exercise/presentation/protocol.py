"""Presentation exercise interface."""

from typing import Protocol

from .. import protocol

# =================================================
# Presentation exercise parameters DTO interface
# =================================================


class PresentationConfigProtocol(
    protocol.HasItemCount,
    protocol.HasDisplayOrder,
    Protocol,
):
    """Presentation exercise perform configuration DTO interface."""


# =================================================
# Presentation exercise case DTO interface
# =================================================


class PresentationCaseProtocol(
    protocol.HasExerciseStatus,
    Protocol,
):
    """Presentation exercise case DTO interface."""
