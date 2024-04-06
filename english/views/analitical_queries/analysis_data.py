from django.db.models import Count

from english.models import WordModel

ANALYSIS_INDICATORS = {
    'word_count': 'Общее количество слов',
    'study_word': 'Слова на изучении',
    'repeat_word': 'Слова на повторении',
    'examination_word': 'Слова на проверке знания',
    'know_word': 'Изученные слова',
    'count_favorites': 'Количество избранных слов всего',
    'study_favorites': 'Количество избранных слов в изучении',
}


def get_favorites_analysis_data(user_id):
    favorites_analysis_data = dict()
    manager = WordModel.objects.filter(user_id=user_id)

    favorites_analysis_data.update(
        manager.aggregate(
            count_favorites=Count('favorites')
        )
    )

    return favorites_analysis_data


def get_common_analysis_data(user_id):
    common_analysis_data = dict()
    manager = WordModel.objects.filter(user_id=user_id)

    common_analysis_data.update(
        manager.aggregate(
            word_count=Count('words_eng'),
        )
    )

    return common_analysis_data
