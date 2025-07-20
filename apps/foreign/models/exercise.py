"""Defines foreign app exercise type model."""

from django.contrib.contenttypes.fields import GenericRelation

from apps.main.models import BaseExercise
from apps.users.models import Transaction


class ForeignExercise(BaseExercise):
    """Foreign app exercise type model."""

    transactions = GenericRelation(
        Transaction,
        related_query_name='foreign_exercise',
    )

    class Meta:
        """Model configuration."""

        db_table = 'foreign_exercise'
