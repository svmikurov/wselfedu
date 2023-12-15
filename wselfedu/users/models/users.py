from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
