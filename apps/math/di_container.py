"""Defines Math app DI container."""

from typing import Any

from dependency_injector import containers, providers
from dependency_injector.providers import Dependency
from wse_exercises.core.math import RandomOperandGenerator

from apps.core.storage.services.iabc import TaskStorageProto
from apps.study.servises.checker import StrTaskChecker
from apps.users.services.award import AwardService

from .presenters.assigned import AssignedCalculationPresenter
from .presenters.calculation import CalculationPresenter
from .services.calculation import CalcService


class MathAppContainer(containers.DeclarativeContainer):
    """DI container for Math app dependencies."""

    # External dependencies
    task_storage: Dependency[TaskStorageProto[Any]] = providers.Dependency()
    # TODO: Update `AwardService` to interface.
    award_service: Dependency[AwardService] = providers.Dependency()

    # Internal providers
    random_operand_generator = providers.Factory(
        RandomOperandGenerator,
    )
    calculation_exercise_service = providers.Factory(
        CalcService,
        operand_generator=random_operand_generator,
    )
    str_task_checker = providers.Factory(
        StrTaskChecker,
    )

    calc_presenter = providers.Factory(
        CalculationPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
        task_checker=str_task_checker,
    )
    assigned_calc_presenter = providers.Factory(
        AssignedCalculationPresenter,
        exercise_service=calculation_exercise_service,
        task_storage=task_storage,
        task_checker=str_task_checker,
        award_service=award_service,
    )
