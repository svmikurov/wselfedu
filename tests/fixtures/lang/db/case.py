"""English translation fixtures."""

import uuid

import pytest

from ..no_db import translations as fixtures


@pytest.fixture
def case_uuid() -> uuid.UUID:
    """Provide Word study presentation case."""
    return fixtures.TRANSLATION_CASE_UUID
