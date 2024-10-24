"""Glossary exercise."""

from contrib.exercise import Exercise
from glossary.models import Glossary
from glossary.queries.lookup_params import GlossaryLookupParams


class GlossaryExerciseGUI(Exercise):
    """Glossary GUI app exercise."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the exercise."""
        super().__init__(*args, **kwargs)

    model = Glossary
    lookup_params = GlossaryLookupParams

    def create_task(self) -> None:
        """Create task."""
        super().create_task()
        self.question_text = self.item.term
        self.answer_text = self.item.definition
