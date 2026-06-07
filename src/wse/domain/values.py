"""Domain value objects."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Presentation:
    """Value object for a text presentation exercise task."""

    question_text: str
    answer_text: str


@dataclass(frozen=True, slots=True)
class Option:
    """Option value object for a selection."""

    value: int
    text: str

    def __str__(self) -> str:
        return self.text

    def to_tuple(self) -> tuple[int, str]:
        """Get tuple representation."""
        return (self.value, self.text)


@dataclass(frozen=True, slots=True)
class Testing:
    """Value object for a testing exercise task."""

    question_text: str
    question_value: int
    options: list[Option]


@dataclass(frozen=True, slots=True)
class AnswerCheck:
    """Value object for a answer check."""

    question_value: int
    answer_value: int


@dataclass(frozen=True, slots=True)
class CheckingResult:
    """Value object for a answer check result."""

    is_correct: bool
