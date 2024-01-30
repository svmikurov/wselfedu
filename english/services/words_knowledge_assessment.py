#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
# Запросы в базу данных осуществляется посредством Django QuerySet API.
#
"""Модуль для оценки пользователем и учета уровня знания слов в приложении.

Модуль содержит функции запросов в базу данных для добавления, обновления и
извлечения уровня знания слов, оцененным пользователем.
Оценка знания имеет ограниченный диапазон, содержащий интервалы.
Каждый интервал используется выборкой слов для отображения на странице
пользователя приложения.
У каждого пользователя свои оценки слов, данные им и доступные только ему.
Приложение содержит следующие интервалы: изучение, повторение, проверка.
"""

from english.models.words import WordModel, WordUserKnowledgeRelation
from users.models import UserModel

MIN_KNOWLEDGE_ASSESSMENT = 0
MAX_STUDYING_VALUE = 6
MAX_REPETITION_VALUE = 8
MAX_EXAMINATION_VALUE = 10
MAX_KNOWLEDGE_ASSESSMENT = 11
"""Значения оценки уровня знания слова пользователем
"""


def get_numeric_value(assessment):
    """Преобразуй строковое представление уровня знания в диапазон чисел
     этого уровня.
     """
    value = []
    if 'studying' in assessment:
        value1 = [*range(MIN_KNOWLEDGE_ASSESSMENT, MAX_STUDYING_VALUE + 1)]
        value += value1
    if 'repetition' in assessment:
        value2 = [*range(MAX_STUDYING_VALUE + 1, MAX_REPETITION_VALUE + 1)]
        value += value2
    if 'examination' in assessment:
        value3 = [*range(MAX_REPETITION_VALUE + 1, MAX_EXAMINATION_VALUE + 1)]
        value += value3
    if 'learned' in assessment:
        value4 = [*range(MAX_EXAMINATION_VALUE + 1, MAX_KNOWLEDGE_ASSESSMENT + 1)]
        value += value4
    return value


def get_knowledge_assessment(word_id, user_id):
    """Получи или создай в базе данных оценку пользователем знание слова.
       При создании оценки, оценка рана "0".
    """
    if user_id and word_id:
        knowledge_assessment_obj, is_create = (
            WordUserKnowledgeRelation.objects.get_or_create(
                word=WordModel.objects.get(pk=word_id),
                user=UserModel.objects.get(pk=user_id),
            )
        )
        knowledge_assessment = knowledge_assessment_obj.knowledge_assessment
        return knowledge_assessment


def get_word_knowledge_assessment(user_id: int, word_id: int) -> int:
    """Получи из базы данных оценку знания слова пользователем.
    """
    assessment = WordUserKnowledgeRelation.objects.filter(
        user_id=user_id, word_id=word_id
    ).values_list('knowledge_assessment', flat=True)[0]
    return assessment


def update_word_knowledge_assessment(user_pk, word_pk, new_assessment):
    """Обнови в базе данных оценку знания слова пользователем, в пределах
       допустимого диапазона.
    """
    if (MIN_KNOWLEDGE_ASSESSMENT
            <= new_assessment
            <= MAX_KNOWLEDGE_ASSESSMENT):
        WordUserKnowledgeRelation.objects.filter(
            word_id=word_pk, user_id=user_pk,
        ).update(knowledge_assessment=new_assessment)
