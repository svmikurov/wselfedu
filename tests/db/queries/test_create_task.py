"""Defines test to story created task into database."""

import pytest
from wse_exercises.core import MathEnum
from wse_exercises.core.math import (
    SimpleCalcAnswer,
    SimpleCalcConditions,
    SimpleCalcConfig,
    SimpleCalcQuestion,
    SimpleCalcTask,
)

from apps.math.models import MathExercise
from apps.users.models import CustomUser
from services.db.task_service import TaskDBService
from utils.sql.report.reporter import SQLReporter


@pytest.fixture
def math_exercise() -> MathExercise:
    """Fixture providing simple math exercise."""
    return MathExercise.objects.create(name='adding')


@pytest.fixture
def simple_math_task_dto() -> SimpleCalcTask:
    """Fixture providing simple math task DTO."""
    return SimpleCalcTask(
        config=SimpleCalcConfig(min_value=1, max_value=9),
        conditions=SimpleCalcConditions(operand_1=3, operand_2=4, time=30),
        question=SimpleCalcQuestion(text='3 + 4'),
        answer=SimpleCalcAnswer(number=12),
        exercise_name=MathEnum.ADDING,
    )


@pytest.mark.skip('Add "math_calculation_task" table to DB')
@pytest.mark.django_db
def test_create_task(
    user: CustomUser,
    math_exercise: MathExercise,
    simple_math_task_dto: SimpleCalcTask,
    debug_reporter: SQLReporter,
) -> None:
    """Test the creation simple math task onto database."""
    exercise = MathExercise.objects.get(
        name=simple_math_task_dto.exercise_name,
    )

    debug_reporter.start_act()

    TaskDBService().add_task(
        user=user,
        task_dto=simple_math_task_dto,
        content_type=exercise,
    )

    debug_reporter.end_act()
