"""Repositories protocols."""

from typing import Protocol

from contracts.entity.general import HasResourceIdentifier

# =================================================
# Update progress repository protocol
# =================================================


class ProgressUpdateConditionsProtocol(
    HasResourceIdentifier,
    Protocol,
):
    """Update progress conditions protocol."""

    delta: int
