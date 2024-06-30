from django.db.models import F

from english.models import WordLearningStories, WordModel


def collect_statistics(task) -> None:
    """Add word display to statistics.

    Count word display at ``display_count`` fild of
    :func:`english.models.word_analytic.WordLearningStories` model.

    Parameters
    ----------
    task : `english.EnglishTranslateExercise`
        Contain task data.
    """
    story, _ = WordLearningStories.objects.get_or_create(
        word=WordModel.objects.get(id=task.word_id)
    )
    story.display_count = F('display_count') + 1
    story.save()
