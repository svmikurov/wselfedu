"""Exercise elements."""

from config.constants import PROGRES_STEPS, PROGRESS_MAX, PROGRESS_MIN
from foreign.models import Word, WordProgress
from users.models import UserApp


class WordAssessment:
    """Assessment of item study."""

    def __init__(self, user: UserApp, word: Word) -> None:
        """Construct the assessment."""
        self.user = user
        self.word = word

    def update(self, action: str) -> None:
        """Update item assessment."""
        assessment_delta = PROGRES_STEPS[action]
        progress, _ = WordProgress.objects.get_or_create(
            user=self.user, word=self.word
        )
        updated_assessment = progress.progress + assessment_delta

        if PROGRESS_MIN <= updated_assessment <= PROGRESS_MAX:
            progress.progress = updated_assessment
            progress.save(update_fields=['progress'])
