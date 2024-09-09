"""Glossary exercise.

Specific for rest api requests.
"""


class GlossaryExercise:
    """Glossary exercise."""

    def __init__(self, exercise_conditions: dict) -> None:
        """Construct the exercise."""
        self.exercise_conditions = exercise_conditions

    @property
    def data(self) -> dict:
        """Exercise data."""
        results = {
            'term_id': '',
            'term': '',
            'definition': '',
            'category': '',
        }
        return results

    @property
    def errors(self) -> object:
        return False
