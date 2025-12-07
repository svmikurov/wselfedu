"""Word study test case data."""

import uuid
from typing import TypeAlias

from rest_framework.exceptions import ErrorDetail

from apps.lang.types import ProgressCase

# Progress cases
# --------------

VALID_PAYLOAD: ProgressCase = {
    'case_uuid': uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4'),
    'is_known': True,
}

InvalidPayload: TypeAlias = dict[str, uuid.UUID | bool]
SerializerErrors: TypeAlias = dict[str, list[ErrorDetail]]
InvalidPayloadCases: TypeAlias = list[tuple[InvalidPayload, SerializerErrors]]

INVALID_PAYLOAD: InvalidPayloadCases = [
    (
        {'case_uuid': 'invalid', 'is_known': True},  # type: ignore[dict-item]
        {
            'case_uuid': [
                ErrorDetail(
                    string='Must be a valid UUID.',
                    code='invalid',
                ),
            ]
        },
    ),
    (
        {'case_uuid': uuid.uuid4(), 'is_known': 'invalid'},  # type: ignore[dict-item]
        {
            'is_known': [
                ErrorDetail(string='Must be a valid boolean.', code='invalid')
            ]
        },
    ),
    (
        {},
        {
            'case_uuid': [
                ErrorDetail(
                    string='Обязательное поле.',
                    code='required',
                )
            ],
        },
    ),
]

ServiceErrors: TypeAlias = ValueError | LookupError
ServiceErrorCases: TypeAlias = list[tuple[ServiceErrors, str]]

SERVICE_ERROR: ServiceErrorCases = [
    (ValueError('Invalid progress'), 'Invalid progress'),
    (LookupError('Case not found'), 'Case not found'),
]
