"""Users app DTOs."""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from apps.users.models import Person


class RewardDTO(BaseModel):
    """Reward DTO."""

    student: Person
    amount: Decimal

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        frozen=True,
        extra='forbid',
    )
