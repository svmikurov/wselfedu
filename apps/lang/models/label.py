"""language discipline labels."""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

LABEL_LENGTH = 70


class LangLabel(models.Model):
    """Language discipline label."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=LABEL_LENGTH,
        unique=True,
        verbose_name='Лейбл',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Лейбл дисциплины.'
        verbose_name = 'Лейблы дисциплины'
        db_table = 'lang_label'

    def __str__(self) -> str:
        """Get string representation."""
        return self.name

    def get_absolute_url(self) -> str:
        """Get object url path."""
        url: str = reverse_lazy('lang:label_detail', kwargs={'pk': self.pk})
        return url
