"""Defines the relationship between the user and the task."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class UserTasks(models.Model):
    """Model of the relationship between a user and a tasks."""

    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
    )

    # Generic relationship
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_uid = models.UUIDField()
    content_object = GenericForeignKey(
        'content_type',
        'object_uid',
    )

    class Meta:
        """Configure the model."""

        indexes = [models.Index(fields=['content_type', 'object_uid'])]
