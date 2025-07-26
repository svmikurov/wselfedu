"""Defines reward transaction proxy model on math exercise."""

from apps.users.models import Transaction


class MathTransaction(Transaction):
    """reward transaction proxy model on math exercise"""

    class Meta:
        """Model configuration."""

        proxy = True
        db_table = 'math"."transaction'
