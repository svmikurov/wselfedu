"""Defines Lang syntax task."""

from django.db import models

from apps.main.models import BaseTask


class SyntaxTask(BaseTask):
    """Foreign syntax task model."""

    exercise = models.ForeignKey(
        'ForeignExercise',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model configuration."""

        db_table = 'lang"."syntax_task'
