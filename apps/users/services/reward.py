"""Student reward service."""

from typing import override

from utils import decorators

from .abstract import AbstractRewardService

__all__ = ('CalculationRewardService',)


# NOTE: It's experimental reward service definition
class CalculationRewardService(AbstractRewardService):
    """Calculation exercise reward service."""

    @override
    @decorators.log_unimplemented_call
    def increment(self, resource_pk: int, mentorship_pk: int) -> None:
        """Add reward."""

    @override
    @decorators.log_unimplemented_call
    def decrement(self, resource_pk: int, mentorship_pk: int) -> None:
        """Remove reward."""
