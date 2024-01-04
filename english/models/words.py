from django.db import models
from django.utils import timezone

from english.models.categories import CategoryModel
from english.models.labels import LabelModel
from english.models.lessons import LessonModel
from english.models.sources import SourceModel
from users.models import UserModel


class WordModel(models.Model):
    """Англо-русский словарь"""

    # Количество слов для перевода, может быть словом, словосочетанием,
    # частью предложения, целым предложением.
    NOT_CHOICE_WORD_COUNT = 'NC'
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
        null=True, blank=True,
        related_name='vocabulary_added_by_user',
    )
    words_eng = models.CharField(
        max_length=75,
        null=False, blank=False,
        verbose_name='Слово на английском',
    )
    words_rus = models.CharField(
        max_length=75,
        null=False, blank=False,
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
        default=NOT_CHOICE_WORD_COUNT,
        verbose_name='Количество слов',
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
    # A field that displays how the user rates his knowledge of this word
    knowledge_assessment = models.ManyToManyField(
        UserModel,
        through='WordUserKnowledgeRelation',
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Англо-русский словарь'
        verbose_name_plural = 'Англо-русский словарь'
        ordering = ['words_eng']

    def __str__(self):
        return self.words_eng


class WordLabelRelation(models.Model):
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    label = models.ForeignKey(LabelModel, on_delete=models.CASCADE)


class WordUserKnowledgeRelation(models.Model):
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    knowledge_assessment = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        default=0,
    )


def get_knowledge_assessment(word_id, user_id):
    knowledge_assessment_obj, is_create = (
        WordUserKnowledgeRelation.objects.get_or_create(
            word=WordModel.objects.get(pk=word_id),
            user=UserModel.objects.get(pk=user_id),
        )
    )
    knowledge_assessment = knowledge_assessment_obj.knowledge_assessment
    return knowledge_assessment
