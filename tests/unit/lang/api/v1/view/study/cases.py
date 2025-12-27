"""Word study test case data."""

import uuid

from rest_framework.exceptions import ErrorDetail

from apps.lang.types import ProgressCase

type InvalidPayload = dict[str, uuid.UUID | bool]
type InvalidPayloadCases = list[tuple[InvalidPayload, SerializerErrors]]
type SerializerErrors = dict[str, list[ErrorDetail]]

type ServiceErrors = ValueError | LookupError
type ServiceErrorCases = list[tuple[ServiceErrors, str]]

# Progress cases
# --------------

VALID_PAYLOAD: ProgressCase = {
    'case_uuid': uuid.UUID('5b518a3e-45a4-4147-a097-0ed28211d8a4'),
    'is_known': True,
}


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

SERVICE_ERROR: ServiceErrorCases = [
    (ValueError('Invalid progress'), 'Invalid progress'),
    (LookupError('Case not found'), 'Case not found'),
]
