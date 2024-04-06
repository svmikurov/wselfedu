from django.db.models import Count, F

from english.models import WordModel

ANALYSIS_INDICATORS = {
    'word_count': 'Общее количество слов',
    'study_word_count': 'Слова на изучении',
    'repeat_word_count': 'Слова на повторении',
    'examination_word': 'Слова на проверке знания',
    'know_word': 'Изученные слова',
    'count_favorites': 'Количество избранных слов всего',
    'study_favorites': 'Количество избранных слов в изучении',
}


def get_favorites_analytic_data(user_id):
    """Get user's favorites word data.
    """
    favorites_analytic_data = dict()
    queryset = WordModel.objects.filter(
        wordsfavoritesmodel__user_id=user_id,
        wordsfavoritesmodel__word_id=F('pk'),
    )

    count_favorites = queryset.aggregate(
        count_favorites=Count('favorites'),
    )
    study_favorites = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=range(0, 7),
    ).aggregate(study_favorites=Count('favorites'))
    repeat_favorites = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=(7, 8)
    ).aggregate(repeat_favorites=Count('favorites'))
    examination_favorites = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=(9, 10)
    ).aggregate(examination_favorites=Count('favorites'))
    know_favorites = queryset.filter(
        worduserknowledgerelation__knowledge_assessment=11
    ).aggregate(know_favorites=Count('favorites'))

    favorites_analytic_data.update(count_favorites)
    favorites_analytic_data.update(study_favorites)
    favorites_analytic_data.update(repeat_favorites)
    favorites_analytic_data.update(examination_favorites)
    favorites_analytic_data.update(know_favorites)

    return favorites_analytic_data


def get_common_analysis_data(user_id):
    """Get user's studies word count.
    """
    common_analysis_data = dict()
    manager = WordModel.objects

    word_count = manager.filter(user_id=user_id).aggregate(word_count=Count('words_eng'))

    queryset = manager.filter(
        worduserknowledgerelation__user_id=user_id,
        worduserknowledgerelation__word_id=F('pk'),
    )

    study_word_count = queryset.filter(
        knowledge_assessment__in=range(0, 7)
    ).aggregate(study_word_count=Count('knowledge_assessment'))
    repeat_word_count = queryset.filter(
        knowledge_assessment__in=(7, 8)
    ).aggregate(study_word_count=Count('knowledge_assessment'))
    examination_word_count = queryset.filter(
        knowledge_assessment__in=(9, 10)
    ).aggregate(study_word_count=Count('knowledge_assessment'))
    know_word_count = queryset.filter(
        knowledge_assessment=11
    ).aggregate(study_word_count=Count('knowledge_assessment'))

    common_analysis_data.update(word_count)
    common_analysis_data.update(study_word_count)
    common_analysis_data.update(repeat_word_count)
    common_analysis_data.update(examination_word_count)
    common_analysis_data.update(know_word_count)
    return common_analysis_data
