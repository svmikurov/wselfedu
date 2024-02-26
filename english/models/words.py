from django.db import models
from django.utils import timezone

from english.models.categories import CategoryModel
from english.models.sources import SourceModel
from users.models import UserModel


class WordModel(models.Model):
    """Англо-русский словарь"""

    # Количество слов для перевода, может быть: словом, словосочетанием,
    # частью предложения, целым предложением, любым количеством слов.
    WORD_COUNT = [
        ('NC', 'Любое количество слов'),    # not choices
        ('OW', 'Слово'),                    # one word
        ('CB', 'Словосочетание'),           # combination
        ('PS', 'Часть предложения'),        # part sentence
        ('ST', 'Предложение'),              # sentence
    ]
    DEFAULT_WORD_COUNT = WORD_COUNT[0][0]

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='vocabulary_added_by_user',
    )
    words_eng = models.CharField(
        max_length=75,
        verbose_name='Слово на английском',
    )
    words_rus = models.CharField(
        max_length=75,
        verbose_name='Слово на русском',
    )
    source = models.ForeignKey(
        SourceModel,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='get_source',
        verbose_name='Источник',
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name='Категория',
    )
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    word_count = models.CharField(
        max_length=2,
        choices=WORD_COUNT,
        default=DEFAULT_WORD_COUNT,
        verbose_name='Количество слов',
    )
    # A field that displays how the user rates his knowledge of this word
    # Оценка пользователем уровня знания слова
    knowledge_assessment = models.ManyToManyField(
        UserModel,
        through='WordUserKnowledgeRelation',
        blank=True,
        related_name='word_knowledge'
    )
    # Does it word favorites for show?
    favorites = models.ManyToManyField(
        UserModel,
        through='WordsFavoritesModel',
        blank=True,
        related_name='word_favorites',
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Англо-русский словарь'
        verbose_name_plural = 'Англо-русский словарь'
        # сортировка задана для избегания противоречивых результатов в
        # неупорядоченном списке при разбивке на страницы (пангинации)
        # Источник - замечание при тестировании
        ordering = ['pk']

    def __str__(self):
        return self.words_eng


class WordUserKnowledgeRelation(models.Model):
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE,)
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
        return (f'{self.user} оценивает знание слова {self.word} '
                f'на {self.knowledge_assessment}')


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
