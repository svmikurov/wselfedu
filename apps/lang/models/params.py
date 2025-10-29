"""Word study params model."""

from django.contrib.auth import get_user_model
from django.db import models


class Params(models.Model):
    """Word study default params model."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_params',
    )
    category = models.ForeignKey(
        'LangCategory',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='category_params',
    )
    label = models.ForeignKey(
        'LangLabel',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Лейбл',
        related_name='label_params',
    )
    word_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Максимальное количество слов',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Параметр изучения слов'
        verbose_name_plural = 'Параметры изучения слов'
        db_table = 'lang_params'
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='word_study_params_unique_user_name',
            )
        ]
