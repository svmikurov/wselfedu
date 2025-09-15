"""User reward service."""
import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import F, OuterRef, Subquery

from apps.study.models import (
    AssignationCompletes,
    ExerciseAssigned,
    ExerciseTaskAward,
)
from apps.users.models import Balance
from apps.users.models.transaction import Transaction

logger = logging.getLogger(__name__)


class AwardService:
    """User reward service."""

    @staticmethod
    def reward(assignation_id: str | int) -> Decimal:
        """Reward the user and return the updated balance."""
        with transaction.atomic():
            award_subquery = ExerciseTaskAward.objects.filter(
                exercise=OuterRef('pk')
            ).values('award')[:1]

            assignation = (
                ExerciseAssigned.objects.select_related(
                    'mentorship__student',
                    'exercise__discipline',
                )
                .select_for_update()
                .annotate(award_value=Subquery(award_subquery))
                .get(pk=assignation_id)
            )

            if not assignation.award_value:
                raise ValueError(
                    f'Award for "{assignation_id}" assignation was not set')

            completion, _ = AssignationCompletes.objects.update_or_create(
                assignation=assignation,
                defaults={
                    'attempt_count': F('attempt_count') + 1,
                    'success_count': F('success_count') + 1,
                },
            )

            balance_total, _ = Balance.objects.update_or_create(
                user=assignation.mentorship.student,
                defaults={
                    'total': F('total') + assignation.award_value,
                },
            )

            balance_total.refresh_from_db()

            Transaction.objects.create(
                user=assignation.mentorship.student,
                amount=assignation.award_value,
                discipline=assignation.exercise.discipline,
                type=Transaction.Operation.REWARD,
            )

        return balance_total.total
