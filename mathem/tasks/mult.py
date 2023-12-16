"""
Contains multiplication task.
The numbers to be multiplied are chosen randomly.
"""
from random import randint

START_RANGE = 2
END_RANGE = 9


class MultTask:
    """Multiplication task."""

    # random operand values are dropped only during initialization
    def __init__(self):
        self.first_operand = randint(START_RANGE, END_RANGE)
        self.second_operand = randint(START_RANGE, END_RANGE)

    def create_task(self):
        text_task = f'{self.first_operand} x {self.second_operand}'
        correct_answer = str(self.first_operand * self.second_operand)
        return text_task, correct_answer
