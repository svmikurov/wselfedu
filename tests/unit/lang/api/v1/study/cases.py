"""Word study test case data."""

import uuid
from typing import TypeAlias

from rest_framework.exceptions import ErrorDetail

from apps.lang.types import WordProgressT

# Progress cases
# --------------

VALID_PAYLOAD: WordProgressT = {
    'case_uuid': uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4'),
    'progress_type': 'known',
}

InvalidPayload: TypeAlias = dict[str, uuid.UUID | str]
SerializerErrors: TypeAlias = dict[str, list[ErrorDetail]]
InvalidPayloadCases: TypeAlias = list[tuple[InvalidPayload, SerializerErrors]]

INVALID_PAYLOAD: InvalidPayloadCases = [
    (
        {'case_uuid': 'invalid', 'progress_type': 'known'},
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
        {'case_uuid': uuid.uuid4(), 'progress_type': 'invalid'},
        {
            'progress_type': [
                ErrorDetail(
                    string='Значения invalid нет среди допустимых вариантов.',
                    code='invalid_choice',
                )
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
            'progress_type': [
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
