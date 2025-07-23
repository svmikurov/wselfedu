"""Defines Lang app task model."""

from django.db import models

from apps.main.models import BaseTask


class TranslationTestTask(BaseTask):
    """Word translation test task model."""

    exercise = models.ForeignKey(
        'LangExercise',
        on_delete=models.CASCADE,
    )

    class Meta:
        """Model configuration."""

        db_table = 'lang_translation_test_task'
