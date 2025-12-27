"""Study progress schemas."""

from pydantic import BaseModel


class UpdateProgress(BaseModel):
    """Update study progress schema.

    Serializes the response data.
    """

    case_uuid: str
    is_known: bool
