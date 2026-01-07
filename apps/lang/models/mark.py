"""Translation relationship with the marker model."""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

LABEL_LENGTH = 70


class LangMark(models.Model):
    """Language discipline mark."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=LABEL_LENGTH,
        unique=True,
        verbose_name='Маркер',
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

        verbose_name = 'Маркер'
        verbose_name_plural = 'Маркеры'
        db_table = 'lang_mark'

    def __str__(self) -> str:
        """Get string representation."""
        return self.name

    def get_absolute_url(self) -> str:
        """Get object url path."""
        url = reverse_lazy('lang:mark_detail', kwargs={'pk': self.pk})
        return str(url)


class EnglishMark(models.Model):
    """English translation relationship with the marker."""

    user = models.ForeignKey(
        'users.Person', on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Перевод',
    )
    mark = models.ForeignKey(
        'LangMark',
        on_delete=models.CASCADE,
        verbose_name='Маркер',
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

        unique_together = ['translation', 'mark']
        verbose_name = 'Маркировка перевода'
        verbose_name_plural = 'Маркировки переводов'
        db_table = 'lang_english_mark'
