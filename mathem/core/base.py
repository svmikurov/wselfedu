from random import randint


class RandomOperandDescriptor:
    """Descriptor for random value of the operand."""

    min_value = 1
    max_value = 10

    def __get__(self, instance, owner):
        return randint(self.min_value, self.max_value)


class MathematicsTask:
    """Base parent class for simple math calculations with two operands.

    Override in child classes math calculations:
    - attribute ``operator``
    - method ``calculate``
    For example:
    -----------
        operator = '+'
        @classmethod
        def calculate(cls, fist_operand, second_operand):
            return int(fist_operand) + int(second_operand)
    """
    question = 'Пока ничего не заданно.'
    fist_operand = RandomOperandDescriptor()
    second_operand = RandomOperandDescriptor()
    operator = None
    calculation = None

    def __init__(self):
        self.set_question()
        self.set_calculation()

    @classmethod
    def set_question(cls):
        question = f'{cls.fist_operand} {cls.operator} {cls.second_operand}'
        setattr(cls, 'question', question)

    @classmethod
    def calculate(cls, fist_operand, second_operand):
        """Override this method in math calculations with two operands."""

    @classmethod
    def set_calculation(cls):
        fist_operand, second_operand = cls.question.split(f' {cls.operator} ')
        calculation = cls.calculate(fist_operand, second_operand)
        setattr(cls, 'calculation', calculation)

    def get_question(self):
        return self.question

    def evaluate_solution(self, user_solution):
        return str(self.calculation) == str(user_solution)


class AdditionTask(MathematicsTask):
    """Class of addition of two operands."""

    operator = '+'

    @classmethod
    def calculate(cls, fist_operand, second_operand):
        return int(fist_operand) + int(second_operand)


class SubtractionTask(MathematicsTask):
    """Class of subtraction of two operands."""

    operator = '-'

    @classmethod
    def calculate(cls, fist_operand, second_operand):
        return int(fist_operand) - int(second_operand)


class MultiplicationTask(MathematicsTask):
    """Class of multiplication of two operands."""

    operator = '*'

    @classmethod
    def calculate(cls, fist_operand, second_operand):
        return int(fist_operand) * int(second_operand)
