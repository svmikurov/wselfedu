"""Defines abstract base exercise model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.users.models import Transaction


class BaseExercise(models.Model):
    """Absract base exercise model."""

    name = models.CharField(
        max_length=30,
    )
    transactions = GenericRelation(
        Transaction,
    )

    class Meta:
        """Model configuration."""

        abstract = True
