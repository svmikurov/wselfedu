"""User exercise settings."""

from django.contrib.auth import get_user_model
from django.db import models


class Settings(models.Model):
    """User exercise settings."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    question_timeout = models.FloatField(
        blank=True,
        null=True,
    )
