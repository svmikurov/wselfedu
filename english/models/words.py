from django.db import models
from django.utils import timezone

from english.models.categories import CategoryModel
from english.models.labels import LabelModel
from english.models.lessons import LessonModel
from english.models.sources import SourceModel
from users.models import UserModel


class WordModel(models.Model):
    """Англо-русский словарь"""

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='vocabulary_added_by_user',
    )
    words_eng = models.CharField(
        max_length=60,
        null=False, blank=False,
        verbose_name='Слово на английском',
    )
    words_rus = models.CharField(
        max_length=60,
        null=False, blank=False,
        verbose_name='Слово на русском',
    )
    source = models.ForeignKey(
        SourceModel,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Источник',
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Категория',
    )
    lesson = models.ForeignKey(
        LessonModel,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Тема урока',
    )
    labels = models.ManyToManyField(
        LabelModel,
        through='WordLabelRelation',
        blank=True,
        verbose_name='Метки',
        related_name='labels',
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Англо-русский словарь'
        verbose_name_plural = 'Англо-русский словарь'


class WordLabelRelation(models.Model):
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    label = models.ForeignKey(LabelModel, on_delete=models.CASCADE)
