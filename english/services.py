"""
Модуль для работы с базой данных.
"""

from config.settings import MIN_KNOWLEDGE_ASSESSMENT, MAX_KNOWLEDGE_ASSESSMENT

from english.models.words import (
    WordsFavoritesModel,
    WordModel,
    WordUserKnowledgeRelation,
)
from users.models import UserModel

###############################################################################
# Handle current words favorites words to learn.                              #
###############################################################################


def add_word_to_favorites(user_id, word_id):
    """Add word to favorites.
    """
    is_word_already_favorite = WordsFavoritesModel.objects.filter(
        user_id=user_id, word_id=word_id,
    ).exists()
    if not is_word_already_favorite:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )


def remove_word_from_favorites(user_pk, word_pk):
    """Remove word from favorites.
    """
    try:
        word = WordsFavoritesModel.objects.filter(user=user_pk, word=word_pk)
    except ValueError:
        print('Такого слова нет в избранных.')
    else:
        word.delete()


def is_word_in_favorites(user_id, word_id) -> bool:
    """Return the True if the word is the favorites,
       otherwise return the False.
    """
    is_favorites = WordsFavoritesModel.objects.filter(
        user=user_id, word=word_id,
    ).exists()
    return is_favorites


###############################################################################
# End Handle current words favorites words to learn.                          #
###############################################################################
# Handle users' word knowledge assessment.                                    #
###############################################################################


def get_or_create_knowledge_assessment(word_id, user_id):
    """Получи или создай в базе данных оценку пользователем знание слова.
       При создании оценки, оценка рана "0".
    """
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
    """Обнови в базе данных оценку знания слова пользователем.
    """
    if (MIN_KNOWLEDGE_ASSESSMENT
            <= new_assessment
            <= MAX_KNOWLEDGE_ASSESSMENT):
        WordUserKnowledgeRelation.objects.filter(
            word_id=word_pk, user_id=user_pk,
        ).update(knowledge_assessment=new_assessment)


###############################################################################
# End Handle users' word knowledge assessment.                                #
###############################################################################
