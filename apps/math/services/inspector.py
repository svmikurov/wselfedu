"""Defines mathematical application task inspectors."""

from typing import Protocol, TypeVar

T_contr = TypeVar('T_contr', contravariant=True)
A_contr = TypeVar('A_contr', contravariant=True)


class ITaskInspector(Protocol[T_contr, A_contr]):
    """Protocol for task inspector."""

    @staticmethod
    def check(correct_answer: T_contr, user_answer: A_contr) -> bool:
        """Check the user answer."""


class SimpleTaskInspector(ITaskInspector[int, int]):
    """Protocol for task inspector."""

    @staticmethod
    def check(correct_answer: int, user_answer: int) -> bool:
        """Check the user answer."""
        return bool(correct_answer == user_answer)
