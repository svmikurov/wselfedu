"""Defines math app exercise type model."""

from django.contrib.contenttypes.fields import GenericRelation

from apps.main.models import BaseExercise
from apps.users.models import Transaction


class MathExercise(BaseExercise):
    """Math app exercise type model."""

    transactions = GenericRelation(
        Transaction,
        related_query_name='math_exercise',
    )

    class Meta:
        """Model configuration."""

        db_table = 'math_exercise'
