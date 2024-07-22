"""Модуль для оценки пользователем и учета уровня знания слов в приложении.

Модуль содержит функции запросов в базу данных для добавления, обновления и
извлечения уровня знания слов, оцененным пользователем.
Оценка знания имеет ограниченный диапазон, содержащий интервалы.
Каждый интервал используется выборкой слов для отображения на странице
пользователя приложения.
У каждого пользователя свои оценки слов, данные им и доступные только ему.
Приложение содержит следующие интервалы: изучение, повторение, проверка.
"""

from english.models import WordUserKnowledgeRelation

MIN_KNOWLEDGE_ASSESSMENT = 0
MAX_STUDYING_VALUE = 6
MAX_REPETITION_VALUE = 8
MAX_EXAMINATION_VALUE = 10
MAX_KNOWLEDGE_ASSESSMENT = 11
"""Значения оценки уровня знания слова пользователем
"""
WORD_STUDY_ASSESSMENTS = {
    'S': [*range(MIN_KNOWLEDGE_ASSESSMENT, MAX_STUDYING_VALUE + 1)],
    'R': [*range(MAX_STUDYING_VALUE + 1, MAX_REPETITION_VALUE + 1)],
    'E': [*range(MAX_REPETITION_VALUE + 1, MAX_EXAMINATION_VALUE + 1)],
    'K': [MAX_KNOWLEDGE_ASSESSMENT],
}
"""A literal representation of an knowledge assessment
(`dict[str, list[int]]`).

key : `str`
    A literal representation of an knowledge assessment.
    Where:
        'S' - is a word in the process of studied;
        'R' - word in process of repetition;
        'E' - is a word in the process of examination;
        'K' - the word has been studied.
value : `int`
    A digital range representation of an knowledge assessment.
"""


def get_knowledge_assessment(word_id, user_id):
    """Получи или создай в базе данных оценку пользователем знание слова.
       При создании оценки, оценка рана "0".
    """
    if user_id and word_id:
        knowledge_assessment_obj, is_create = (
            WordUserKnowledgeRelation.objects.get_or_create(
                word_id=word_id,
                user_id=user_id,
            )
        )
        knowledge_assessment = knowledge_assessment_obj.knowledge_assessment
        return knowledge_assessment


def update_word_knowledge_assessment(word_pk, user_pk, new_assessment):
    """Обнови в базе данных оценку знания слова пользователем, в пределах
       допустимого диапазона.
    """
    if (MIN_KNOWLEDGE_ASSESSMENT
            <= new_assessment
            <= MAX_KNOWLEDGE_ASSESSMENT):
        WordUserKnowledgeRelation.objects.filter(
            word_id=word_pk, user_id=user_pk,
        ).update(knowledge_assessment=new_assessment)


def get_numeric_value(knowledge_assessments):
    """Преобразуй строковое представление уровня знания в диапазон чисел
     этого уровня.
     """
    value = []
    for assessment in WORD_STUDY_ASSESSMENTS:
        if assessment in knowledge_assessments:
            value += WORD_STUDY_ASSESSMENTS[assessment]
    return value
