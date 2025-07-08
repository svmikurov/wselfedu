"""Defines a DI container for injecting dependencies into math app."""

from dependency_injector import containers, providers
from wse_exercises.core import MATH_EXERCISES
from wse_exercises.core.math import RandomOperandGenerator, SimpleCalcTask
from wse_exercises.core.math.base.services import OperandGenerator

from services.storage.task import TaskCache

from ..users.services.balance import BalanceService
from .models.simple import SimpleTask
from .services.db import SimpleCalcDBService
from .services.factories import ExercisesFactory
from .services.inspector import SimpleTaskInspector
from .services.simple import SimpleCalcService


class MathAppContainer(containers.DeclarativeContainer):
    """DI container for injecting dependencies into math app."""

    # Balance service

    balance_service = providers.Factory(
        BalanceService,
    )

    # Storage services

    simple_task_cache = providers.Singleton(
        TaskCache[SimpleCalcTask],
    )
    simple_task_db = providers.Singleton(
        SimpleCalcDBService,
        manager=SimpleTask.objects,
    )

    # Exercise service

    random_operand_generator: OperandGenerator = RandomOperandGenerator()
    exercise_factory = providers.Factory(
        ExercisesFactory,
        exercises=MATH_EXERCISES,
        operand_generator=random_operand_generator,
    )
    simple_inspector = providers.Factory(
        SimpleTaskInspector,
    )

    # Exercise with two operands
    simple_calc_service = providers.Factory(
        SimpleCalcService,
        exercise_factory=exercise_factory,
        db=simple_task_db,
        cache=simple_task_cache,
        inspector=simple_inspector,
        balance_service=balance_service,
    )
