from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class UserModel(AbstractUser, models.Model):
    updated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('users:detail', kwargs={'pk': self.pk})
