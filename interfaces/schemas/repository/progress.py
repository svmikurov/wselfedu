"""Progress repositories interface."""

from pydantic import Field

from contracts.schemas.fields import ResourceIdentifierField

# =================================================
# Update progress repository schema
# =================================================


class ProgressUpdateConditions(
    ResourceIdentifierField,
):
    """Progress update conditions."""

    delta: int = Field(
        description='Update progress delta',
    )
