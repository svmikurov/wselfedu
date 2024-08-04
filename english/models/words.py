from django.db import models
from django.utils import timezone

from english.models.categories import CategoryModel
from english.models.sources import SourceModel
from users.models import UserModel


class WordModel(models.Model):
    """English-Russian dictionary."""

    NOT_CHOICES = 'NC'
    ONE_WORD = 'OW'
    COMBINATION = 'CB'
    PART_SENTENCE = 'PS'
    SENTENCE = 'ST'
    WORD_COUNT = [
        ('NC', 'Любое количество слов'),
        ('OW', 'Слово'),
        ('CB', 'Словосочетание'),
        ('PS', 'Часть предложения'),
        ('ST', 'Предложение'),
    ]

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='user_word',
        verbose_name='Пользователь, который изучает слово',
    )
    """User who studies the word.
    """
    mentor = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mentor_word',
        verbose_name='Наставник, который добавил слово.',
    )
    """User who added the word.
    """
    word_eng = models.CharField(
        max_length=75,
        verbose_name='Слово на английском',
        help_text='Не более 75 символов.',
    )
    word_rus = models.CharField(
        max_length=75,
        verbose_name='Слово на русском',
        help_text='Не более 75 символов.',
    )
    source = models.ForeignKey(
        SourceModel,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='get_source',
        verbose_name='Источник',
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    word_count = models.CharField(
        max_length=2,
        choices=WORD_COUNT,
        default=NOT_CHOICES,
        verbose_name='Количество слов',
    )
    # A field that displays how the user rates his knowledge of this
    # word
    knowledge_assessment = models.ManyToManyField(
        UserModel,
        through='WordUserKnowledgeRelation',
        blank=True,
        related_name='word_knowledge',
    )
    # Does it word favorites for show?
    favorites = models.ManyToManyField(
        UserModel,
        through='WordsFavoritesModel',
        blank=True,
        related_name='word_favorites',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        verbose_name = 'Англо-русский словарь'
        verbose_name_plural = 'Англо-русский словарь'
        ordering = ['pk']

    def __str__(self):
        return self.word_eng


class WordUserKnowledgeRelation(models.Model):
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    knowledge_assessment = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
    )

    class Meta:
        unique_together = [['word', 'user']]
        verbose_name = 'Оценка пользователем знания слова'
        verbose_name_plural = 'Оценки пользователем знания слова'

    def __str__(self):
        return self.knowledge_assessment


class WordsFavoritesModel(models.Model):
    """Model for store users favorites words."""

    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['word', 'user']]
        verbose_name = 'Избранное слово'
        verbose_name_plural = 'Избранные слова'

    def __str__(self):
        return f'Слово {self.word} избрано {self.user}'
