from django.db import models


class LessonModel(models.Model):
    name = models.CharField(
        max_length=30,
        null=False, blank=False,
        verbose_name='Тема урока',
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
