"""Foreign word study app analytic module."""

from django.db.models import F

from config.constants import DISPLAY_COUNT
from english.models import WordLearningStories, WordModel
from task.tasks import ForeignWordTranslateExercise


def collect_statistics(task: ForeignWordTranslateExercise) -> None:
    """Add word display to statistics.

    Count word display at ``display_count`` fild of
    :func:`english.models.word_analytic.WordLearningStories` model.

    Parameters
    ----------
    task : `ForeignWordTranslateExercise`
        Contain task data.

    """
    story, _ = WordLearningStories.objects.get_or_create(
        word=WordModel.objects.get(id=task.word_id)
    )
    story.display_count = F(DISPLAY_COUNT) + 1
    story.save()
