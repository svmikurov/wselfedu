from django.db.models import Manager

from english.models.words import WordsFavoritesModel, WordModel, \
    WordUserKnowledgeRelation
from users.models import UserModel


def filter_objects(func: callable):
    """Decorator for filter objects by field name."""
    def inner(objects: Manager, fields_filter=(), *args, **kwargs):
        return func(objects, *args, **kwargs).filter(*fields_filter)
    return inner


@filter_objects
def all_objects(objects_manager: Manager):
    return objects_manager.all()


###############################################################################
# Handle current words favorites words to learn.                              #
###############################################################################


def add_word_to_favorites(user_id, word_id):
    """Add word to favorites."""
    is_word_already_favorite = WordsFavoritesModel.objects.filter(
        user_id=user_id, word_id=word_id,
    ).exists()
    if not is_word_already_favorite:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )


def remove_word_from_favorites(user_pk, word_pk):
    """Remove word from favorites."""
    try:
        word = WordsFavoritesModel.objects.filter(user=user_pk, word=word_pk)
    except ValueError:
        print('Такого слова нет в избранных.')
    else:
        word.delete()


def is_word_in_favorites(user_id, word_id) -> bool:
    """Return the True if the word is the favorites,
       otherwise return the False."""
    is_favorites = WordsFavoritesModel.objects.filter(
        user=user_id, word=word_id,
    ).exists()
    return is_favorites


######################################################
# End Handle current words favorites words to learn. #
######################################################


def get_knowledge_assessment(word_id, user_id):
    knowledge_assessment_obj, is_create = (
        WordUserKnowledgeRelation.objects.get_or_create(
            word=WordModel.objects.get(pk=word_id),
            user=UserModel.objects.get(pk=user_id),
        )
    )
    knowledge_assessment = knowledge_assessment_obj.knowledge_assessment
    return knowledge_assessment
