"""Analytics of foreign word study."""

from django.db.models import F

from config.constants import DISPLAY_COUNT
from foreign.exercise.translate import TranslateExercise
from foreign.models import Word, WordAnalytics


def collect_statistics(task: TranslateExercise) -> None:
    """Collect the display count in statistics.

    Count word display at ``display_count`` fild of
    :func:`foreign.models.word_analytic.WordLearningStories` model.

    :params TranslateExercise task: Task data.
    """
    story, _ = WordAnalytics.objects.get_or_create(
        word=Word.objects.get(id=task.word_id)
    )
    story.display_count = F(DISPLAY_COUNT) + 1
    story.save()
