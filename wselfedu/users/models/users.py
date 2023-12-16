from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy


class UserModel(AbstractUser):

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user:detail', kwargs={'pk': self.pk})
