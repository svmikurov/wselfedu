"""Repositories protocols."""

from typing import Protocol

from ports.contract.entity.general import HasResourceIdentifier

# =================================================
# Update progress repository protocol
# =================================================


class ProgressUpdateConditionsProtocol(
    HasResourceIdentifier,
    Protocol,
):
    """Update progress conditions protocol."""

    delta: int
