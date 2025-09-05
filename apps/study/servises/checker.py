"""String task answer checker."""

from apps.study.servises.iabc import BaseStrTaskChecker


class StrTaskChecker(BaseStrTaskChecker):
    """String task answer checker."""

    def check(self, correct_answer: str, user_answer: str) -> bool:
        """Check the answer."""
        is_correct = bool(user_answer == correct_answer)
        return is_correct
