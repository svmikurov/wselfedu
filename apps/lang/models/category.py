"""Language discipline category."""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

CATEGORY_LENGTH = 70


class LangCategory(models.Model):
    """Language discipline category."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=CATEGORY_LENGTH,
        unique=True,
        verbose_name='Категория',
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

        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'lang_category'

    def __str__(self) -> str:
        """Get string representation."""
        return self.name

    def get_absolute_url(self) -> str:
        """Get object url path."""
        url = reverse_lazy('lang:category_detail', kwargs={'pk': self.pk})
        return str(url)
