from django.db.models import Count, F, Q

from english.models import WordModel
from english.services.word_knowledge_assessment import WORD_STUDY_ASSESSMENTS

ANALYSIS_INDICATORS = {
    'word_count': 'Общее количество слов',
    'study_word_count': 'Слова на изучении',
    'repeat_word_count': 'Слова на повторении',
    'examination_word_count': 'Слова на проверке знания',
    'know_word_count': 'Изученные слова',
    # favorites words
    'favorites_count': 'Количество избранных слов всего',
    'study_favorites_count': 'Количество избранных слов в изучении',
    'repeat_favorites_count': 'Количество избранных слов на повторении',
    'examination_favorites_count': 'Количество избранных слов на проверке',
    'know_favorites_count': 'Количество избранных слов изучено',
}


def get_favorites_analytic_data(user_id):
    """Get user's favorites word data.
    """
    favorites_analytic_data = dict()
    stages = WORD_STUDY_ASSESSMENTS
    queryset = WordModel.objects.filter(
        wordsfavoritesmodel__user_id=user_id,
        wordsfavoritesmodel__word_id=F('pk'),
    )
    favorites_count = queryset.aggregate(
        favorites_count=Count('*'),
    )
    study_favorites_count = queryset.filter(
            worduserknowledgerelation__knowledge_assessment__in=stages['S'],
    ).aggregate(study_favorites_count=Count('*'))
    repeat_favorites_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=stages['R'],
    ).aggregate(repeat_favorites_count=Count('*'))
    examination_favorites_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=stages['E'],
    ).aggregate(examination_favorites_count=Count('*'))
    know_favorites_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment=stages['K'][0],
    ).aggregate(know_favorites_count=Count('*'))

    favorites_analytic_data.update(favorites_count)
    favorites_analytic_data.update(study_favorites_count)
    favorites_analytic_data.update(repeat_favorites_count)
    favorites_analytic_data.update(examination_favorites_count)
    favorites_analytic_data.update(know_favorites_count)

    return favorites_analytic_data


def get_common_analysis_data(user_id):
    """Get user's studies word count.
    """
    common_analysis_data = dict()
    stages = WORD_STUDY_ASSESSMENTS
    manager = WordModel.objects
    queryset = manager.filter(
        worduserknowledgerelation__user_id=user_id,
        worduserknowledgerelation__word_id=F('pk'),
    )
    not_assessment_words = Q(
        user_id=user_id
    ) & ~Q(
        worduserknowledgerelation__user_id=user_id,
        worduserknowledgerelation__word_id=F('pk'),
    )

    word_count = manager.filter(
        user=user_id
    ).aggregate(word_count=Count('*'))
    study_word_count = manager.filter(
        Q(
            worduserknowledgerelation__user_id=user_id,
            worduserknowledgerelation__word_id=F('pk'),
            worduserknowledgerelation__knowledge_assessment__in=stages['S'],
        ) | not_assessment_words
    ).aggregate(study_word_count=Count('*'))
    repeat_word_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=stages['R'],
    ).aggregate(repeat_word_count=Count('*'))
    examination_word_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment__in=stages['E'],
    ).aggregate(examination_word_count=Count('*'))
    know_word_count = queryset.filter(
        worduserknowledgerelation__knowledge_assessment=stages['K'][0],
    ).aggregate(know_word_count=Count('*'))

    common_analysis_data.update(word_count)
    common_analysis_data.update(study_word_count)
    common_analysis_data.update(repeat_word_count)
    common_analysis_data.update(examination_word_count)
    common_analysis_data.update(know_word_count)
    return common_analysis_data
