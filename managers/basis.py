"""Defines basis model manager."""

import uuid

from django.db import models


class TaskManager(models.Manager[models.Model]):
    """Task model manager."""

    def get_task(self, task_uid: uuid.UUID) -> models.Model:
        """Get task."""
        task = self.filter(uid=task_uid).first()

        if not isinstance(task, models.Model):
            raise TypeError

        return task
