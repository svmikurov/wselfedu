"""Defines abstract base task model."""

import uuid

from django.db import models


class BaseTask(models.Model):
    """Abstract base model for task."""

    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )

    class Meta:
        """Class configuration."""

        abstract = True
