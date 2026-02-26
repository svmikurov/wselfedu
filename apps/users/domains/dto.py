"""Users app DTOs."""

from decimal import Decimal

from apps.core.domains.base_dto import BaseDTO


class RewardDTO(BaseDTO):
    """Reward DTO."""

    student_pk: int
    amount: Decimal
