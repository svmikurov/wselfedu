"""The mathematical calculate exercise."""

import operator
import os
from abc import ABC, abstractmethod

from random import randint
from typing import Any

from dotenv import load_dotenv

load_dotenv('.env_vars/.env.wse')

POINTS_FOR_THE_TASK = int(os.getenv('POINTS_FOR_THE_TASK', 0))
"""The number of points awarded for a correctly completed task,
by default (`int`).
"""
MAX_POINTS_BALANCE = int(os.getenv('MAX_POINTS_BALANCE', 0))
"""The maximum allowed accumulation of points on the user's balance.
(`int`)
"""


class BaseExercise(ABC):
    """Base exercise class."""

    @abstractmethod
    def create_task(self) -> None:
        """Create a task."""
        pass

    @property
    @abstractmethod
    def task_data(self) -> dict[str, str]:
        """Task data."""
        pass

    @property
    @abstractmethod
    def cache_data(self) -> dict[str, Any]:
        """Cache a task data."""
        pass


class CalculationExercise(BaseExercise):
    """Calculation exercise with two operands."""

    _OPS = {
        'add': operator.add,
        'sub': operator.sub,
        'mul': operator.mul,
    }
    """Alias representation of mathematical operators."""
    _OP_SIGNS = {
        'add': '+',
        'sub': '-',
        'mul': 'x',
    }
    """Alias representation of mathematical sign."""

    def __init__(
        self,
        *,
        calc_type: str,
        min_value: int = 1,
        max_value: int = 9,
    ) -> None:
        """Construct calculation exercise."""
        self._calc_type = calc_type
        self._min_value = min_value
        self._max_value = max_value
        self._operand1: int | None = None
        self._operand2: int | None = None
        self._question_text: str | None = None
        self._answer_text: str | None = None

    def create_task(self) -> None:
        """Create a task."""
        self._operand1 = randint(self._min_value, self._max_value)
        self._operand2 = randint(self._min_value, self._max_value)
        math_sign = self._OP_SIGNS.get(self._calc_type)

        self._question_text = f'{self._operand1} {math_sign} {self._operand2}'
        self._answer_text = str(
            self._OPS[self._calc_type](self._operand1, self._operand2)
        )

    @property
    def task_data(self) -> dict[str, str]:
        """Task data to render."""
        return {
            'question': self._question_text,
            'answer': self._answer_text,
        }

    @property
    def cache_data(self) -> dict[str, Any]:
        """Task data to cache."""
        return {
            'calc_type': self._calc_type,
            'operand1': self._operand1,
            'operand2': self._operand2,
        }
