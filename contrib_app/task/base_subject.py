class BaseSubject:
    """Subject base class."""

    def __init__(self):
        self._question_text = None
        self._answer_text = None

    def set_subject_params(self, **kwargs):
        """Set subject task params."""
        self._set_task_solution()

    def _set_task_solution(self):
        """Create and set question and answer text."""
        pass

    def get_question_text(self):
        """Get a text representation of the task question."""
        self._check_attr(self._question_text)
        return self._question_text

    def get_answer_text(self):
        """Get a text representation of the task answer."""
        self._check_attr(self._answer_text)
        return self._answer_text

    @staticmethod
    def _check_attr(attr):
        """Check if the attribute is set."""
        if not attr:
            raise ValueError('The subject params has not been set')
