"""Word study case fixtures."""

import uuid

import pytest

from apps.lang import types


@pytest.fixture
def case_uuid() -> uuid.UUID:
    """Provide Word study presentation case."""
    return uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4')


@pytest.fixture
def presentation() -> types.PresentationDataT:
    """Provide presentation data."""
    return {
        'definition': 'house',
        'explanation': 'дом',
        'info': {'progress': 7},
    }


@pytest.fixture
def presentation_case(
    case_uuid: uuid.UUID,
    presentation: types.PresentationDataT,
) -> types.PresentationCaseT:
    """Provide Word study presentation case."""
    return {
        'case_uuid': case_uuid,
        **presentation,
    }
