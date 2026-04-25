"""Protocol for validator interface."""

from typing import Protocol, TypeVar

RequestData_contra = TypeVar('RequestData_contra', contravariant=True)
Validated_co = TypeVar('Validated_co', covariant=True)


class RequestValidatorProtocol(
    Protocol[RequestData_contra, Validated_co],
):
    """Protocol for request data validator interface."""

    def validate(self, data: RequestData_contra) -> Validated_co:
        """Validate request data."""
