"""Presentation exercise hendler DI "smoke" tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ports.contract.types.handler import PresentationHandlerT


def test_create_presentation_task(
    presentation_handler: PresentationHandlerT,
) -> None:
    """Test presentation request handler smoke."""
