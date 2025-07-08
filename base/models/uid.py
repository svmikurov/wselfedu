"""Defines models with UID primary key."""

import uuid

from django.db import models


class UIDModel(models.Model):
    """Defines base models with UID primary key."""

    uid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        """Configure the model."""

        abstract = True
